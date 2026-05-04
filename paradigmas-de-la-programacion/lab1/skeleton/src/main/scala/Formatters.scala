object Formatters {

  val stopwords: Set[String] = Set(
    "the", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can't",
    "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further",
    "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
    "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
    "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
    "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me",
    "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
    "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "re", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
  )

  def totalScore(posts: List[FileIO.Post]): Int = {
    posts.foldLeft(0) { case (acc, (_, _, _, _, _, score)) => acc + score }
  }
  def formatTopPosts(posts: List[FileIO.Post]): String = {
    val topPosts = posts.take(5)
    if (topPosts.isEmpty) "No hay posts disponibles."
    else {
      topPosts.zipWithIndex.map { case ((subreddit, title, _, date, url, _), idx) =>
        s"${idx + 1}. - Subreddit: r/$subreddit\n   - Titulo: $title\n   - Fecha: $date\n   - URL: $url\n"
      }.mkString("\n")
    }
  }

  // Pure function to format posts from a subscription
  def formatSubscription(subredditName: String, posts: List[FileIO.Post]): String = {
    val header = s"\n${"=" * 80}\nSubreddit: r/$subredditName (${posts.length} posts)\n${"=" * 80}"
    val formattedPosts = posts.zipWithIndex.map { case (post, idx) =>
      formatSinglePost(idx + 1, post)
      }.mkString("\n")
    header + "\n" + formattedPosts
  }

  // funcion auxiliar para formatear posts individualmente
  def formatSinglePost(index: Int, post: FileIO.Post): String = {
    val (subreddit, title, selftext, date, url, score) = post
    s"""
    |--- Post #$index ---
    |Subreddit: r/$subreddit
    |Title: $title
    |Date: $date 
    |Selftext: ${selftext.replace("\n", " ").take(80)}
    |${"-"*80}
    |Url: $url
    |Score: $score
    """.stripMargin
  }

  def formatSubscriptionReport(subredditName: String,posts: List[FileIO.Post],frequencies: List[(String, Int)]): String = {
    val scoreSum = totalScore(posts)
    val wordsOutput =
      if (frequencies.isEmpty) "Sin palabras frecuentes."
      else frequencies.take(20).map { case (word, count) => s"- $word: $count" }.mkString("\n")
    s"""
       |## r/$subredditName
       |- Score total acumulado: $scoreSum
       |
       |### Palabras mas frecuentes
       |$wordsOutput
       |
       |### Primeros 5 posts
       |${formatTopPosts(posts)}
       |""".stripMargin
  }
  // Ejercicio 5

  //Visor de frecuencias de palabras, formatea la salida para mostrar las 20 palabras mas frecuentes con su conteo
  def formatWordFrequencies(subredditName: String, frequencies: List[(String, Int)]): String = {
    val header = s"Frecuencias de palabras en r/$subredditName"
    val body = frequencies
      .take(20)
      .map { case (word, count) => s"$word -> $count" }
      .mkString("\n")

    s"$header\n$body"
  }

  // Fun aux que transforma texto a lista de palabras
  // Elimina espacios, signos de puntuacion y convierte a minusculas
  def extractWords(text: String): List[String] = {
    text
      .split("\\W+")
      .filter(_.nonEmpty)
      .toList
  }

  //Filtra palabras que empiezan con mayuscula
  def startsWithUpper(word: String): Boolean = {
    word.nonEmpty && word.head.isUpper
  }

  //Filtro para palabras que no esten en la lista de stopwords
  def isNotStopword(word: String, stopwords: Set[String]): Boolean = {
    !stopwords.contains(word.toLowerCase)
  }

  //Pone en minuscula para normalizar
  def normalizeWord(word: String): String = {
    word.toLowerCase
  }

  //Agrupa palabras con su frecuencia, usa groupby como pide el ejercicio
  //devuelve un mapa con palabra -> frecuencia
  def countFrequencies(words: List[String]): Map[String, Int] = {
    words
      .groupBy(identity) // agrupa palabras iguales
      .map { case (word, list) => word -> list.size } // cuenta frecuencia de cada palabra
  }

  //Funcion integrada que hace todo el proceso de conteo de palabras
  //Se realiza un solo conteo con los dos filtros: "comiencen con mayúscula" y "no sean stopwords"
  def subredditWordFrequencies(posts: List[FileIO.Post], stopwords: Set[String]): List[(String, Int)] = {

    //Toma los post y extrae palabras de titulo y selftext
    val allWords = posts.flatMap { case (_, title, selftext, _, _, _) =>
      extractWords(title) ++ extractWords(selftext)
    }

    // Toma solo las palabras que empiezan con mayuscula y no son stopwords
    val filteredWords = allWords.filter(word => startsWithUpper(word) && isNotStopword(word, stopwords))
    
    // Normaliza las palabras a minuscula para contar correctamente
    val normalizedWords = filteredWords.map(normalizeWord)

    countFrequencies(normalizedWords).toList.sortBy { case (word, count) => (-count, word) }
  }
}