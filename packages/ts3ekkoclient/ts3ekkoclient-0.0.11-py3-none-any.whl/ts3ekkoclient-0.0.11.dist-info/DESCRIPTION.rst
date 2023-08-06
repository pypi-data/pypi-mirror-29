Projektarbeit
=============

Sprache: python3.6

Entwicklung eines TeamSpeak3 (TS3) Bots, welcher mit gleicher (bestehender) Konfiguration in mehreren Channeln eines TS3
Servers gleichzeit aktiv ist.

Applikation
-----------

ts3ekko
~~~~~~~

* nimmt Commands über das Chat Interface war (shell-ähnlich)

 * bsp syntax: `!queue  [-s|--source-type=<type>] [-p|--position=<pos>] <uri>*`
 * bsp: `!queue -s youtube -p 1 youtube.com/watch?v=0xC0FFEE youtube.com/watch?v=0xdlqwidoiw`


Control Commands
''''''''''''''''

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Info
   * - `!spawn`
     - Spawned neue Instanz des Bots im Channel, in dem der Invoker aktuell ist (Übermittlung via privater Nachricht
       an irgendeine andere Instanz auf dem Server)
   * - `!despawn`
     - Despawned die Instanz, zu der dieser Command gesendet wurde
   * - `!join`
     - Bewegt den Bot in den Channel des Invokers. [CHANGE: command hinzugefügt]



Audio Commands
''''''''''''''

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Info
   * - `!queue [-p|--position=<pos>] <uri>*`
     - Fügt neuen Track der instanz-gebundenen Queue zu. Als Quellen sind YouTube sowie lokal (filesystem) möglich (`-s`) [CHANGE: `--source-type` entfernt, da mpv über auto-detection verfügt]

   * - `!skip [<count>]`
     - Überspringt Anzahl von Tracks in queue. Defaults zum nächsten Track (skip aktuellen)
   * - `!media [queue]`
     - Zeigt Informationen über aktuellen Track an. Wenn `queue` keyword angegeben ist, dann werden Informationen
       über die Tracks in der Queue angezeigt
   * - `!mediaalias set <aliasname> <uri>*`
     - Erstellt einen Alias für eine beliebige Anzahl von URIs. Alias kann anstelle von URIs verwendet werden,
       dafür $aliasname schreiben. Media Alias sind nicht an eine Bot Instanz gebunden.
   * - `!mediaalias get <aliasname>`
     - Zeigt Informationen (Inhalt, Ersteller) zum Alias an
   * - `!mediaalias delete <aliasname>`
     - Löscht den Alias
   * - `!mediaalias append <aliasname> <uri>*`
     - Hängt Tracks an den Inhalt des Alias an
   * - `!pausemedia`
     - Pausiert aktuelle Wiedergabe
   * - `!resumemedia`
     - Fährt mit Wiedergabe fort
   * - `!clearqueue`
     - Entfernt alle Tracks aus der Queue
   * - `!volume reset`
     - Setzt Volume der Bot Instanz auf den Standardwert zurück
   * - `!volume <percent>`
     - Setzt Volume der Bot Instant auf den gewünschten Prozentwert

Text Helper Commands
''''''''''''''''''''

Hierbei handelt es sich um eine Art Text-Alias/Command System. Nutzer können einen beliebigen Text (z.B. Links oder
Erklärungen) an einen Alias hängen. Dieser Alias kann dann als Bot-Command verwendet werden. Sollte eine Nachricht
dem Alias gleichen, dann wird der Bot den damit verbunden Text in den selben Kommunikationschannel schreiben.
So müssen Links oder Erklärungen nicht immer neu kopiert und in den Chat geschrieben werden,
der Alias reicht (gesehen von der Benutzerseite).

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Info
   * - `!textalias set [-p|--permanent] <aliasname> <value>`
     - Erstellt einen Bot-Instanz gebundenen (ungebunden/permanent durch `-p`) Alias
   * - `!textalias get [-p|--permanent] <aliasname>`
     - Liest den Inhalt eines Bot-Instanz gebundenen (ungebunden/permanent durch `-p`) Alias
       (ggf. mit Zusatzinformationen bzgl. Ersteller) aus
   * - `!textalias delete [-p|--permanent] <aliasname>`
     - Löscht einen Bot-Instanz gebundenen (ungebunden/permanent durch `-p`) Alias
   * - `!textalias list-temporary`
     - Listet alle Alias auf, die an die aktuelle Bot-Instanz gebunden sind
   * - `!textalias list-permanent`
     - Listet alle Alias auf, die nicht an die aktuelle Bot-Instanz gebunden sind (ungebunden/permanent)
   * - `!~<aliasname> <value>`
     - Kurzform für `!textalias set`, nur Bot-Instanz gebundene Alias
   * - `!~<aliasname>`
     - Aufruf des Alias

Permissions
'''''''''''

Es soll möglich sein, Befehle nur bestimmten Personen oder Personengruppen zugänglich zu machen.
Als Identifikationsmerkmal werden dafür die TS3 Eigenschaften des Command Invokers benutzt (Server Gruppen,
Channel Gruppen, Identität, etc).

Ein *mögliches* Command Interface für Permissions könnte wie folgt aussehen. Diese Commands wurden mit dem Hintergrund
zusammengestellt, dass es eine feste Menge von Permissions gibt, welche jegliche zu regulierenden Commands abdeckt.
Jede Permission ist eindeutig über einen alphanumerischen Namen (inklusive Unterstriche, Punkte) identifizierbar
(folgt '<permission>' genannt). Punkte in Namen von Permissions werden zur hierarchischen Strukturierung verwendet
(Bsp: audio.mediaalias.append).

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Info
   * - `!permission add <permission> [-i|--identity | -s|--servergroup | -c|--channelgroup] <identifier>`
     - Fügt eine Identität, Server- oder Channel Gruppe zur Liste der erlaubten Entitäten für diese Permission hinzu
   * - `!permission delete <permission> [-i|--identity | -s|--servergroup | -c|--channelgroup]  <identifier>`
     - Entfernt eine Identität, Server- oder Channel Gruppe von der Liste der erlaubten Entitäten für diese Permission
   * - `!permission get <permission>`
     - Zeige alle assozierten Entitäten der Permission
   * - `!permission list [-r] <permission-path>`
     - Zeige Namen aller direkten Permissions in diesem Pfad (Punkt-Separierung), `-r` für rekursive Darstellung
   * - `!permission info <permission-name>`
     - Zeige Informationen zur Permission (z.B. Benutzung, verwandte Permissions, Doku)

Ob dieses Command Interface in diesem Umfang oder dieser Art implementiert wird, ist jedoch noch fraglich.


ts3ekkomanage
~~~~~~~~~~~~~

* kontrolliert die verschiedenen docker container für die einzelnen channel
* spawn von neuen containern für angeforderte channel (`!spawn`)
* de-spawn von containern für channel, in denen der bot nicht mehr erwünscht ist (`!despawn`)



Deployment
----------

* Vagrant Linux VM (libvirt), provisioniert mit ansible

Docker Images
-------------

TS3 Client + ts3ekko
~~~~~~~~~~~~~~~~~~~~

Dieses Image representiert eine Instanz des Bots. Pro Instanz des Bots wird ein Container dieses Images existieren.

ts3ekkomanage
~~~~~~~~~~~~~

Image für die Managementinstanz des Bots. Nur ein Container dieses Images wird pro TeamSpeak3 Server benötigt.

Vermutlich verwendete, bedeutende Bibliotheken
----------------------------------------------

* ts3query/ts3 für teilweise Interaktion (non-audio/non-settings) mit dem TS3 Client über das ClientQuery interface
* docker-py für die Interaktion von ts3ekkomanage mit dem Docker Daemon
* youtube-dl/vlc (o.Ä.) für das streamen der Medien zu den lokalen Audiodevices

|
|
|
|
|

*README-de.rst*

