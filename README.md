# LectioDocuDumper
Downloader alle filer brugeren har adgang til under Dokumenter i Lectio

Jeg lavede primært dette script så jeg havde adgang til alle undervisningsfiler under eksamen, hvor vi ikke må tilgå internettet.

Bruger Python med requests og BeautifulSoup til at scrappe filerne fra html siden.

Skole id findes i URL (.../lectio/<SKOLE_ID>/...)
Elev id find også i URl når man er på dokument eller skema siderne (...SkemaNy.aspx?type=elev&elevid=<ELEV_ID>)
Session Id findes i Cookies som "ASP.NET_SessionId"
