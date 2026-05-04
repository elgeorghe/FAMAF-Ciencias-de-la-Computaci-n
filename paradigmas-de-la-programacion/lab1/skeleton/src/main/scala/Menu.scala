import scala.io.StdIn
import scala.io.StdIn.readLine


// Menu por consola en sistema de capas
// Este archivo solo contiene funciones auxiliares que llamar en main
//(no es posible mantener un loop tradicional en esquema funcional, workaround)
/*
    Esquema general a implementar:
        Presentacion
        Layer 0
        ----------------------------------------
        Layer 1         --->    muestra Subreddits
        Input-layer-1   --->    Selecciona Subreddit o exit
        ----------------------------------------
        Layer 2         --->    muestra estadisticas, frecuencia de palabras, primeros 5 posts y conteo total de post
        Input-layer-2   --->    Selecciona y muestra post, exit o vuelve a Layer 0 (ver si es posible de forma funcional)
*/

object Menu {
    def getPostsForSubreddit(subredditName: String): List[FileIO.Post] = {
        // Como tus funciones devuelven Option, un for-comprehension es la forma 
        // más elegante y funcional de encadenarlas sin usar if/else
        val pipeline = for {
            subs     <- FileIO.readSubscriptions()
            // Buscamos la URL del subreddit ignorando mayúsculas/minúsculas
            url      <- subs.find(_._1.toLowerCase == subredditName.toLowerCase).map(_._2) 
            feedJson <- FileIO.downloadFeed(url)
            rawPosts <- FileIO.parseFeedToPosts(subredditName, feedJson)
        } yield FileIO.filterValidPosts(rawPosts)
        // Si todo sale bien, extrae la lista. Si en algún paso hubo un error (None), devuelve una lista vacía.
        pipeline.getOrElse(List.empty[FileIO.Post])
    }

    def getWordFrequencies(posts: List[FileIO.Post]): Map[String, Int] = {
    if (posts.isEmpty) {
        Map.empty
    } else {
        // 1. Extraemos todo el texto...
        val allText = posts.map { case (_, title, selftext, _, _, _) => 
            s"$title $selftext" 
        }.mkString(" ")

        // 2. Limpiamos...
        val words = allText.toLowerCase.replaceAll("[^a-záéíóúñ\\s]", "").split("\\s+").filter(_.nonEmpty)

        // 3. Agrupamos... (Esta es la última línea, se retorna automáticamente)
        words.groupBy(identity).view.mapValues(_.length).toMap
        }
    }
    // Pequeña introduccion al parser
    def presentacionAlSistema():Unit = {
        println("¡Bienvenido a FeedParser! por favor selecciona una de las siguientes opciones para comenzar:")
    }

    // Menu de seleccion de Subreddits
    def menuLayer1():Unit = {
        println("Subreddits disponibles: 1-Scala, 2-Learn Programming, 3-Learn Python")
        println("Selecciona un subreddit ingresando 1, 2 o 3:")
        val entrada = readLine().trim() // captura la entrada del usuario, .trim elimina espacios en blanco
        entrada match {

            case "1" =>{
                println("Has seleccionado r/Scala")
                menuLayer2("Scala") //llamar funcion de parseo del sub scala
            }

            case "2" =>{ 
                println("Has seleccionado r/LearnProgramming")
                menuLayer2("Learn Programming") //llamar funcion de parseo del sub learn programming
            }

            case "3" =>{ 
                println("Has seleccionado r/LearnPython")
                menuLayer2("Learn Python") //llamar funcion de parseo del sub learn python
            }

            case _ =>{ 
                println("Opción no válida")
                menuLayer1() //volver a mostrar menu de seleccion de subreddits
            }
        }

    }

    // Menu de seleccion de Posts
    def menuLayer2(subreddit: String):Unit = {
        println(s"\n--- estas explorando r/$subreddit ---")
        println("Opciones:")
        println("1 - ver los ultimos posts")
        println("2 - ver estadisticas")
        println("3 - volver al menu principal")
        println("4 - salir")

        val entradaPost = readLine().trim()

        entradaPost match {
            
            case "1" => {
                println(s"Mostrando los ultimos posts de r/$subreddit...")
                println(Formatters.formatTopPosts(getPostsForSubreddit(subreddit)))
                menuLayer2(subreddit) //volver a mostrar menu de seleccion de posts
            }

            case "2" => {
                println(s"Mostrando estadisticas de r/$subreddit...")
                val posts = getPostsForSubreddit(subreddit)
                val frequencies = getWordFrequencies(posts).toList.sortBy(-_._2)
                println(Formatters.formatSubscriptionReport(subreddit, posts, frequencies))
                menuLayer2(subreddit) //volver a mostrar menu de seleccion de posts
            }

            case "3" => {
                println("Volviendo al menu principal...")
                menuLayer1() //volver al menu de seleccion de subreddits
            }

            case "4" => {
                println("Saliendo...")
            }

            case _ => {
                println("Opción no válida")
                menuLayer2(subreddit) //volver a mostrar menu de seleccion de posts
            }
        }

    }


}