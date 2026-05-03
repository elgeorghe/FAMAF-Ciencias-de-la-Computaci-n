/*
 * fat_fuse_ops.c
 *
 * FAT32 filesystem operations for FUSE (Filesystem in Userspace)
 */

#include "fat_fuse_ops.h"

#include "big_brother.h"
#include "fat_file.h"
#include "fat_filename_util.h"
#include "fat_fs_tree.h"
#include "fat_util.h"
#include "fat_volume.h"
#include <alloca.h>
#include <errno.h>
#include <gmodule.h>
#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>


#define LOG_MESSAGE_SIZE 100
#define DATE_MESSAGE_SIZE 30

void fat_new_log_file(fat_volume vol, const char *log_path) {
    // Verificar que el archivo no existe
    fat_tree_node log_node = fat_tree_node_search(vol->file_tree, log_path);
    if (log_node != NULL) {
        printf("%s ya existe, no se crea nuevamente.\n", log_path);
        return;
    }

    // Obtener el nodo del directorio raíz
    fat_tree_node root_node = fat_tree_node_search(vol->file_tree, "/");
    if (root_node == NULL) {
        fprintf(stderr, "No se pudo encontrar el directorio raíz (/).\n");
        return;
    }

    fat_file parent = fat_tree_get_file(root_node);

    // Crear el nuevo archivo
    fat_file new_log = fat_file_init(vol->table, false, strdup(log_path));
    if (!new_log) {
        fprintf(stderr, "Error al crear el archivo.\n");
        return;
    }

    // Insertar en el árbol de directorios y escribir la dentry
    vol->file_tree = fat_tree_insert(vol->file_tree, root_node, new_log);
    fat_file_dentry_add_child(parent, new_log);

    printf("Archivo %s creado correctamente.\n", log_path);
 
 }

static void now_to_str(char *buf) {
     time_t now = time(NULL);
     struct tm *timeinfo;
     timeinfo = localtime(&now);

     strftime(buf, DATE_MESSAGE_SIZE, "%d-%m-%Y %H:%M", timeinfo);
 }

 static void fat_fuse_log_activity(char *operation_type, fat_file file) {

    const char *user = getlogin();
    if (user == NULL)
    {
        user = "unknown"; //esto esta para manejo de errores
    }
    
    char buf[LOG_MESSAGE_SIZE] = "";
    now_to_str(buf);
    strcat(buf, "\t");
    strcat(buf, user);
    strcat(buf, "\t");
    strcat(buf, file->filepath);
    strcat(buf, "\t");
    strcat(buf, operation_type);
    strcat(buf, "\n");

    fat_volume vol = get_fat_volume();
    fat_tree_node log_node = fat_tree_node_search(vol->file_tree, "/fs.log");
    if (!log_node) {
        fat_new_log_file(vol, "/fs.log");
        log_node = fat_tree_node_search(vol->file_tree, "/fs.log");
        if (!log_node) return;
    }
    
    fat_file log_file = fat_tree_get_file(log_node);
    fat_file parent = fat_tree_get_parent(log_node);

    fat_file_pwrite(log_file, buf, strlen(buf), log_file->dentry->file_size, parent);
    
}

/* Loads directory children from the volume into in-memory tree.
 * Calls function fat_file_read_children which returns
 * a list of files inside a GList. The children were read from the directory
 * entries in the cluster of the directory. This function iterates over the
 * list of children and adds them to the file tree.
 * This operation should be performed only once per directory, the first time
 * readdir is called.
 */
static void fat_fuse_load_directory_children(fat_volume vol, fat_tree_node dir_node) {
    fat_file dir = fat_tree_get_file(dir_node);
    GList *children_list = fat_file_read_children(dir);
    // Add children to tree. TODO handle duplicates
    for (GList *l = children_list; l != NULL; l = l->next) {
        vol->file_tree =
            fat_tree_insert(vol->file_tree, dir_node, (fat_file)l->data);
    }
}


fat_volume fat_fuse_init(fat_volume vol) {
    fat_file root_dir = fat_file_init_orphan_dir("/", vol->table, vol->root_dir_start_cluster);
    vol->file_tree = fat_tree_init();
    vol->file_tree = fat_tree_insert(vol->file_tree, NULL, root_dir);

    // Load the content of / to the tree
    fat_tree_node root_dir_node = fat_tree_node_search(vol->file_tree, "/");
    fat_fuse_load_directory_children(vol, root_dir_node);
    fat_tree_print_preorder(vol->file_tree);

    fat_new_log_file(vol, "/fs.log");

    return vol;
}

/* Get file attributes (file descriptor version) */
int fat_fuse_fgetattr(const char *path, struct stat *stbuf,
                      struct fuse_file_info *fi) {
    fat_file file = (fat_file)fat_tree_get_file((fat_tree_node)fi->fh);
    fat_file_to_stbuf(file, stbuf);
    return 0;
}

/* Load the entire hierarchy of parent directories in the in-memory tree.
 * IMPORTANT: Asumes the rood directory / has been already loaded
 */
static int fat_fuse_load_path(const char *path) {
    fat_volume vol = get_fat_volume();
    size_t len = strlen(path);
    char *prefix = calloc(len + 1, sizeof(char));
    for (size_t i = 1; i <= len; i++) {
        if (path[i] != '/') continue;
        if (path[i] == '\0') break;  // End of path
        // We found a path delimiter /, we take everything up to there
        memcpy(prefix, path, i);
        prefix[i] = '\0';

        fat_tree_node dir_node = fat_tree_node_search(vol->file_tree, prefix);
        if (dir_node == NULL) {
            // This doesn't happen because the parent was added in the
            // previous iteration.
            DEBUG("Directory %s not found in tree\n", prefix);
            errno = ENOENT;
            return -errno;
        }
        fat_file dir = fat_tree_get_file(dir_node);
        if (!fat_file_is_directory(dir)) {
            DEBUG("Directory %s is not a directory\n", prefix);
            errno = ENOTDIR;
            return -errno;
        }
        if (dir->children_read != 1) {
            fat_fuse_load_directory_children(vol, dir_node);
        }
    }
    free(prefix);
    return 0;
}

/* Get file attributes (path version) */
int fat_fuse_getattr(const char *path, struct stat *stbuf) {
    fat_volume vol;
    fat_file file;

    vol = get_fat_volume();

    // Check all parent directories in path are loaded in the tree
    fat_fuse_load_path(path);

    file = fat_tree_search(vol->file_tree, path);
    if (file == NULL) {
        errno = ENOENT;
        return -errno;
    }
    fat_file_to_stbuf(file, stbuf);
    return 0;
}

/* Open a file */
int fat_fuse_open(const char *path, struct fuse_file_info *fi) {
    fat_volume vol;
    fat_tree_node file_node;
    fat_file file;

    vol = get_fat_volume();
    file_node = fat_tree_node_search(vol->file_tree, path);
    if (!file_node)
        return -errno;
    file = fat_tree_get_file(file_node);
    if (fat_file_is_directory(file))
        return -EISDIR;
    fat_tree_inc_num_times_opened(file_node);
    fi->fh = (uintptr_t)file_node;
    return 0;
}

/* Open a directory */
int fat_fuse_opendir(const char *path, struct fuse_file_info *fi) {
    fat_volume vol = NULL;
    fat_tree_node file_node = NULL;
    fat_file file = NULL;

    vol = get_fat_volume();
    file_node = fat_tree_node_search(vol->file_tree, path);
    if (file_node == NULL) {
        return -errno;
    }
    file = fat_tree_get_file(file_node);
    if (!fat_file_is_directory(file)) {
        return -ENOTDIR;
    }
    fat_tree_inc_num_times_opened(file_node);
    fi->fh = (uintptr_t)file_node;
    return 0;
}

/* Add entries of a directory in @fi to @buf using @filler function. */
int fat_fuse_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
                     off_t offset, struct fuse_file_info *fi) {
    fat_volume vol = get_fat_volume();
    errno = 0;
    fat_tree_node dir_node = (fat_tree_node)fi->fh;
    fat_file dir = fat_tree_get_file(dir_node);
    fat_file *children = NULL, *child = NULL;
    int error = 0;

    // Insert first two filenames (. and ..)
    if ((*filler)(buf, ".", NULL, 0) || (*filler)(buf, "..", NULL, 0)) {
        return -errno;
    }
    if (!fat_file_is_directory(dir)) {
        errno = ENOTDIR;
        return -errno;
    }
    if (dir->children_read != 1) {
        fat_fuse_load_directory_children(vol, dir_node);
        if (errno < 0) {
            return -errno;
        }
    }

    children = fat_tree_flatten_h_children(dir_node);
    child = children;
    while (*child != NULL) {
        if (strcmp((*child)->name, "fs.log") != 0)
        {
            error = (*filler)(buf, (*child)->name, NULL, 0);
            if (error != 0) {
                return -errno;
            }
        }

       
        child++;
    }
    return 0;
}

/* Read data from a file */
int fat_fuse_read(const char *path, char *buf, size_t size, off_t offset,
                  struct fuse_file_info *fi) {
    errno = 0;
    int bytes_read;
    fat_tree_node file_node = (fat_tree_node)fi->fh;
    fat_file file = fat_tree_get_file(file_node);
    fat_file parent = fat_tree_get_parent(file_node);

    bytes_read = fat_file_pread(file, buf, size, offset, parent);
    fat_fuse_log_activity("read", file);

    return bytes_read;
}

/* Write data from a file */
int fat_fuse_write(const char *path, const char *buf, size_t size, off_t offset,
                   struct fuse_file_info *fi) {
    fat_tree_node file_node = (fat_tree_node)fi->fh;
    fat_file file = fat_tree_get_file(file_node);
    fat_file parent = fat_tree_get_parent(file_node);

    if (size == 0)
        return 0; // Nothing to write
    if (offset > file->dentry->file_size)
        return -EOVERFLOW;

    fat_fuse_log_activity("write", file);
    return fat_file_pwrite(file, buf, size, offset, parent);
}

/* Close a file */
int fat_fuse_release(const char *path, struct fuse_file_info *fi) {
    fat_tree_node file = (fat_tree_node)fi->fh;
    fat_tree_dec_num_times_opened(file);
    return 0;
}

/* Close a directory */
int fat_fuse_releasedir(const char *path, struct fuse_file_info *fi) {
    fat_tree_node file = (fat_tree_node)fi->fh;
    fat_tree_dec_num_times_opened(file);
    return 0;
}

int fat_fuse_mkdir(const char *path, mode_t mode) {
    errno = 0;
    fat_volume vol = NULL;
    fat_file parent = NULL, new_file = NULL;
    fat_tree_node parent_node = NULL;

    // The system has already checked the path does not exist. We get the parent
    vol = get_fat_volume();
    parent_node = fat_tree_node_search(vol->file_tree, dirname(strdup(path)));
    if (parent_node == NULL) {
        errno = ENOENT;
        return -errno;
    }
    parent = fat_tree_get_file(parent_node);
    if (!fat_file_is_directory(parent)) {
        fat_error("Error! Parent is not directory\n");
        errno = ENOTDIR;
        return -errno;
    }

    // init child
    new_file = fat_file_init(vol->table, true, strdup(path));
    if (errno != 0) {
        return -errno;
    }
    // insert to directory tree representation
    vol->file_tree = fat_tree_insert(vol->file_tree, parent_node, new_file);
    // write file in parent's entry (disk)
    fat_file_dentry_add_child(parent, new_file);
    return -errno;
}

/* Creates a new file in @path. @mode and @dev are ignored. */
int fat_fuse_mknod(const char *path, mode_t mode, dev_t dev) {
    errno = 0;
    fat_volume vol;
    fat_file parent, new_file;
    fat_tree_node parent_node;

    // The system has already checked the path does not exist. We get the parent
    vol = get_fat_volume();
    parent_node = fat_tree_node_search(vol->file_tree, dirname(strdup(path)));
    if (parent_node == NULL) {
        errno = ENOENT;
        return -errno;
    }
    parent = fat_tree_get_file(parent_node);
    if (!fat_file_is_directory(parent)) {
        fat_error("Error! Parent is not directory\n");
        errno = ENOTDIR;
        return -errno;
    }
    new_file = fat_file_init(vol->table, false, strdup(path));
    if (errno < 0) {
        return -errno;
    }
    // insert to directory tree representation
    vol->file_tree = fat_tree_insert(vol->file_tree, parent_node, new_file);
    // Write dentry in parent cluster
    fat_file_dentry_add_child(parent, new_file);
    return -errno;
}

int fat_fuse_utime(const char *path, struct utimbuf *buf) {
    errno = 0;
    fat_file parent = NULL;
    fat_volume vol = get_fat_volume();
    fat_tree_node file_node = fat_tree_node_search(vol->file_tree, path);
    if (file_node == NULL || errno != 0) {
        errno = ENOENT;
        return -errno;
    }
    parent = fat_tree_get_parent(file_node);
    if (parent == NULL || errno != 0) {
        DEBUG("WARNING: Setting time for parent ignored");
        return 0; // We do nothing, no utime for parent
    }
    fat_utime(fat_tree_get_file(file_node), parent, buf);
    return -errno;
}

/* Shortens the file at the given offset.*/
int fat_fuse_truncate(const char *path, off_t offset) {
    errno = 0;
    fat_volume vol = get_fat_volume();
    fat_file file = NULL, parent = NULL;
    fat_tree_node file_node = fat_tree_node_search(vol->file_tree, path);
    if (file_node == NULL || errno != 0) {
        errno = ENOENT;
        return -errno;
    }
    file = fat_tree_get_file(file_node);
    if (fat_file_is_directory(file))
        return -EISDIR;

    parent = fat_tree_get_parent(file_node);
    fat_tree_inc_num_times_opened(file_node);
    fat_file_truncate(file, offset, parent);
    return -errno;
}

int fat_fuse_unlink(const char *path){
    errno = 0;

    //Verificar si el archivo existe
    fat_volume vol = get_fat_volume();
    fat_tree_node node_to_destroy = fat_tree_node_search(vol->file_tree, path);
    if(node_to_destroy == NULL){
        errno = ENOENT;
        return -errno;
    }
    
    //Verificar que no sea un directorio
    fat_file file_to_destroy = fat_tree_get_file(node_to_destroy);
    if(fat_file_is_directory(file_to_destroy)){
        errno = EISDIR;
        return -errno;
    }
    
    fat_file parent = fat_tree_get_parent(node_to_destroy);

    //Marcando Entry como eliminada
    file_to_destroy->dentry->base_name[0] = 0xE5;

    //Escribiendo la entry modificada en disco
    off_t parent_offset = fat_table_cluster_offset(parent->table, parent->start_cluster);
    size_t entry_size = sizeof(struct fat_dir_entry_s);
    off_t entry_offset = parent_offset + (file_to_destroy->pos_in_parent * entry_size);
    size_t written_bytes = full_pwrite(parent->table->fd, file_to_destroy->dentry, entry_size, entry_offset);
    if(written_bytes != entry_size){
        errno = EIO;
        return -errno;
    }

    //Liberando la cadena de clusters
    u32 current_cluster = file_to_destroy->start_cluster;
    while(fat_table_cluster_is_valid(current_cluster)){
        u32 next_cluster = fat_table_get_next_cluster(vol->table, current_cluster);
        if(fat_table_set_next_cluster(vol->table, current_cluster, FAT_CLUSTER_FREE) == -1){
            errno = EPERM;
            return -errno;
        }
        current_cluster = next_cluster;
    }

    //Actualizando el arbol
    vol->file_tree = fat_tree_delete(vol->file_tree, path);

    //Sale sin errores
    return 0;
}

int fat_fuse_rmdir(const char *path){
    errno = 0;

    //Verificando que el directorio exista
    fat_volume vol = get_fat_volume();
    fat_tree_node node_to_destroy = fat_tree_node_search(vol->file_tree, path);
    if(node_to_destroy == NULL){
        errno = ENOENT;
        return -errno;
    }


    fat_file dir_to_destroy = fat_tree_get_file(node_to_destroy);

    //Verificar que sea un directorio
    if(!fat_file_is_directory(dir_to_destroy)){
        errno = ENOTDIR;
        return -errno;
    }


    //Verificar que no sea root
    if(strcmp(path, "/") == 0){
        errno = EPERM;
        return -errno;
    }


    //Verificar que el directorio esta vacio
    if(dir_to_destroy->children_read != 1){
        fat_fuse_load_directory_children(vol, node_to_destroy);
    }
    fat_file *children = fat_tree_flatten_h_children(node_to_destroy);
    int valid_entries = 0;
    if(children != NULL){
        fat_file *child = children;
        while(child != NULL){
            if(strcmp((*child)->name, ".") != 0     &&      strcmp((*child)->name, "..") != 0){
            valid_entries++;
            }
            child++;
        }
        free(children);
    }

    if(valid_entries > 0){
        DEBUG("ERROR: Directory not empty");
        errno = EPERM;
        return -errno;
    }


    //Directorio parent para mas adelante
    fat_file parent = fat_tree_get_parent(node_to_destroy);
    

    //Eliminando entradas "." y ".."
    u32 dir_to_destroy_cluster = dir_to_destroy->start_cluster;
    size_t bytes_per_cluster = fat_table_bytes_per_cluster(vol->table);
    u8 *cluster_buff = alloca(bytes_per_cluster);
    off_t cluster_offset = fat_table_cluster_offset(vol->table, dir_to_destroy_cluster);

    //Leer el cluster del directorio
    if(full_pread(vol->table->fd, cluster_buff, bytes_per_cluster, cluster_offset) != bytes_per_cluster){
        DEBUG("ERROR: Error al leer el cluster del directorio");
        errno = EIO;
        return -errno;
    }

    //Buscando entradas "." y ".."
    fat_dir_entry entries = (fat_dir_entry)cluster_buff;
    for(int i = 0; i < bytes_per_cluster / sizeof(struct fat_dir_entry_s); i++){
        if(entries[i].base_name[0] == 0x00){
            break; //Fin del directorio
        }
        if(entries[i].base_name[0] == 0xE5){
            continue; //Ya fue eliminado
        }

        //Chekear si es "." o ".."
        char name[MAX_FILENAME];
        build_filename(entries[i].base_name, entries[i].extension, name);
        if(strcmp(name, ".") == 0       ||      strcmp(name, "..") == 0){
            entries[i].base_name[0] = 0xE5; //Marcando como eliminado
        }
    }   


    //Reescribiendo el cluster modificado
    if(full_pwrite(vol->table->fd, cluster_buff, bytes_per_cluster, cluster_offset) != bytes_per_cluster){
        DEBUG("ERROR: Error al escribir cluster de directorio");
        errno = EIO;
        return -errno;
    }

    //Borrando la entry en parent
    dir_to_destroy->dentry->base_name[0] = 0xE5;
    off_t parent_offset = fat_table_cluster_offset(parent->table, parent->start_cluster);
    off_t entry_offset = parent_offset + (dir_to_destroy->pos_in_parent * sizeof(struct fat_dir_entry_s));
    if(full_pwrite(parent->table->fd, dir_to_destroy->dentry, sizeof(struct fat_dir_entry_s), entry_offset) != sizeof(struct fat_dir_entry_s)){
        errno = EIO;
        return -errno;
    }


    //Liberando la cadena de clusters del directorio
    u32 current_cluster = dir_to_destroy->start_cluster;
    while(fat_table_cluster_is_valid(current_cluster)){
        u32 next_cluster = fat_table_get_next_cluster(vol->table, current_cluster);
        if(fat_table_set_next_cluster(vol->table, current_cluster, FAT_CLUSTER_FREE) == -1){
            DEBUG("ERROR: Error liberando cluster %u", current_cluster);
        }
        current_cluster = next_cluster;
    }


    //Actualizando el arbol
    vol->file_tree = fat_tree_delete(vol->file_tree, path);

    //Sale sin errores
    return 0;
}