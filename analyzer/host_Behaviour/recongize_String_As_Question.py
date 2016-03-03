from textblob import TextBlob

# How to check wether it is a question or not
# TODO: ? am Ende eines Satze4s
# TODO: Filterung nach Tier / Hierarchie der Frage möglich?

# 1. Wenn im Commentar ein Fragezeichen drin ist && der Author nicht der iAMA-Ersteller ist --> Frage (und merke dir die commentar_id, und die utc)

# 2. Durchsuche alle Comments, die jene commentar_id als parent_id haben (und wenn die Länge aller Kommentare größer 1 ist)

#   2.1. Wenn es einen entsprechenden Folgekommentar gibt und der Author der iAMA-Ersteller ist --> Antwort

#          2.1.1. Dann merke dir die UTC des iAMA-Hosts-Kommentars
#          2.1.2. Berechne die Difference seit Frage-Erstellung mit Antwort-Erstellung des Hosts (dadurch können wir die Response-Time berechnen)
#          2.1.3. Counte hoch, dass HOST geantwortet hat

#   2.2. Wenn nach allen Iterationen kein Folgekommentar des iAMA-Erstellers gefunden werden kann, welcher sich auf jenen Kommentar bezieht, dann counte hoch, dass Host NICHT geantwortet hat.

# Was können wir dadurch insgesamt berechnen?

# 1.1. Die allgemeine Reaktionszeit des iAMA-Erstellers
# 1.2. Das Verhältnis zu gestellten Fragen und Antworten hierauf durch den iAMA-Host

testimonial = TextBlob("How many times have you been complimented on your looks?")


print (testimonial.sentiment)