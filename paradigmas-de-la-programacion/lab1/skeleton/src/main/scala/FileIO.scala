import scala.io.Source
import ujson.Value
import scala.util.{Try, Using}

//necesario ppara formateo de fecha
import java.time.Instant 
import java.time.format.DateTimeFormatter
import java.time.ZoneOffset


object FileIO {
  
  type Subscription = (String, String) // (subredditName, url)
  type Post = (String, String, String, String, String, Int) // (subreddit, title, selftext, date, url, score)


  // Pure function to read subscriptions from a JSON file
  def readSubscriptions(): Option[List[Subscription]] = {
    Try{
      val relativepath = "subscriptions.json"
      // leer el archivo y parsearlo a un objeto Json
      Using(Source.fromFile(relativepath)) { source =>
        val jsonString = source.mkString
        val jsonParseado: Value = ujson.read(jsonString)
        // extraer nombre y url y devolverlos como una tupla
        jsonParseado.arr.map { elemento =>
          val name = elemento("name").str
          val url = elemento("url").str

          //retorno la tupla
          (name, url)
        }.toList
      }.get // Extrae el valor del Using (que devuelve un Try)
    }.toOption // Convierte el Try exterior en Option
  }

  // Pure function to download JSON feed from a URL
  def downloadFeed(url: String): Option[String] = {
    Using(Source.fromURL(url)) { source =>
      source.mkString
      }
  }.toOption

  // Genera una lista de posts individuales, cada lista es un subreddit
  def parseFeedToPosts(subredditName: String, jsonString: String): Option[List[Post]] = {
    Try{
      val json = ujson.read(jsonString)
      val postsArray = json("data")("children").arr
      
      postsArray.map { postJson =>
        val data = postJson("data")
        val title = data("title").str
        val selftext = data("selftext").str
        val postUrl = data("url").str
        val score = data("score").num.toInt

        //date viene como double, necesitamos que sea string para evitar conflicto con Post
        // aprovechamos para formatear
        val createdUtc = data("created_utc").num.toLong
        val instant: Instant = Instant.ofEpochSecond(createdUtc)
        //no borrar la z en el formato, por algun motivo se rompe todo, que cosa asquerosa
        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z").withZone(ZoneOffset.UTC)
        val date: String = formatter.format(instant)

        (subredditName, title, selftext, date, postUrl, score)
      }.toList
    }
  }.toOption

  // conteo de posts fue contado a mano, unico cambio visible es r/scala de 25 a 15 posts
  // habria que revisar post a post por si acaso
  def filterValidPosts(posts: List[Post]): List[Post] = {
    posts.filter { post =>
      val (_, title, selftext, _, _, _) = post
      title.trim.nonEmpty && selftext.trim.nonEmpty
    }
  }
}
