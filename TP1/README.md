## Étudiantes

- Yaye Fatou Niang Dioum
- Fatoumata Bintou Capho Diouf

## Encadrant

Dr Keba Gueye

**Année académique : 2026–2027**

## TP 1 – LE MODÈLE CLIENT-SERVEUR: ***réponses aux questions*** 

## Q1. Combien d’étudiants, d’EC et de notes la base contient-elle ? Schéma des quatre tables.
<img width="574" height="230" alt="image" src="https://github.com/user-attachments/assets/be9a4323-a185-457d-8ed1-17b987975244" />

La base contient **30 étudiants, 6 éléments constitutifs (EC) et 180 notes.**

Le schéma des quatre tables, avec leurs clés primaires (PK) et étrangères (FK, repérées par #), est le suivant :

<img width="475" height="336" alt="image" src="https://github.com/user-attachments/assets/7a946d6f-da1f-4de1-8c58-21d8b4b6326c" />


## Q2. Le client mariadb et le serveur mariadbd sont-ils le même programme ? Montrez-le avec ps -ef | grep -i mariadb.
<img width="501" height="80" alt="image" src="https://github.com/user-attachments/assets/65c14b79-c154-428a-b2b5-ef111fc25865" />

Non. Le client mariadb et le serveur mariadbd sont deux programmes distincts, même lorsqu’ils s’exécutent sur la même machine. La commande ps -ef | grep -i mariadb le montre : après la sortie du client (exit), le processus du serveur mariadbd continue de tourner, ce qui prouve qu’il est indépendant du client.

## Q3. Que signifie le code d’erreur 10061 de la première tentative ? VM1 était-elle joignable ? Le serveur MariaDB fonctionnait-il ?
<img width="452" height="51" alt="image" src="https://github.com/user-attachments/assets/6ff2715d-aa92-4ad9-b14d-47dd18040f78" />


Le code 10061 signifie que la connexion a été refusée, tandis que le code 10060 affiché sur notre capture signifie que le délai d’attente a été dépassé : dans les deux cas, le client n’arrive pas à se connecter au serveur.
Le serveur MariaDB fonctionnait, mais il n’écoutait que sur l’adresse locale 127.0.0.1 ; VM1 n’était donc pas joignable sur le port 3306 depuis le réseau.

## Q4. Différence entre écouter sur 127.0.0.1 et sur 0.0.0.0 ? Pourquoi Ubuntu choisit-il 127.0.0.1 par défaut ?
<img width="542" height="53" alt="image" src="https://github.com/user-attachments/assets/b5802fa1-6ce0-4920-96df-19f5e08d6ef5" />

Écouter sur 127.0.0.1 (localhost) signifie que le serveur n’accepte que les connexions venant de la machine elle-même : l’accès depuis le réseau est refusé. Avec 0.0.0.0, on demande à MariaDB d’écouter sur toutes les interfaces réseau IPv4 disponibles. La configuration par défaut d’Ubuntu retient 127.0.0.1 par mesure de sécurité, pour ne pas exposer la base de données au réseau tant que l’administrateur ne l’a pas décidé.

## Q5. Relevez le résultat de SELECT USER(), CURRENT_USER();. Expliquez la différence entre les deux valeurs.
<img width="398" height="110" alt="image" src="https://github.com/user-attachments/assets/62c27a2f-94ec-47fe-996a-2e3dae80a87d" />


USER ( ) indique l’utilisateur d’origine de la connexion, c’est-à-dire l’identité présentée par le client.
CURRENT_USER ( ) indique le compte MariaDB réellement utilisé par le serveur, celui dont les privilèges sont appliqués.

Résultat relevé : USER ( ) = etudiant@192.168.56.1 et CURRENT_USER ( ) = etudiant@192.168.56.%.

Le compte défini sur le serveur est donc etudiant@192.168.56. %, valable pour toute machine du réseau privé hôte.

## Q6. Avec quel compte Windows pourrait-il se connecter en tant que root depuis le réseau ? Essayez. Pourquoi est-ce une bonne chose ?
<img width="518" height="44" alt="image" src="https://github.com/user-attachments/assets/f490d4e1-2d14-4d54-923a-04fec2ba8b5c" />

Depuis Windows, la tentative de connexion avec le compte root (mariadb -h 192.168.56.11 -u root -p scolarite) échoue, même en saisissant un mot de passe : le serveur répond par l’erreur 1045 (Access denied for user ‘root’@‘192.168.56.1’).

C’est une bonne chose car si root était accessible depuis le réseau, une personne distante pourrait supprimer la base de données, la modifier, créer ou supprimer des utilisateurs, etc.

## Q7. Adresse IP et port source de chaque client. Qui a choisi ces ports, et pourquoi sont-ils différents de 3306 ?

**Client** : VM2
**Adresse IP** : 192.168.56.12
**Port source** : 56066

**Client** : Windows
**Adresse IP** : 192.168.56.1
**Port source** : 51366

Ces ports n’ont pas été choisis par MariaDB. Le serveur écoute sur le port 3306 ; lorsqu’un client se connecte, son système d’exploitation lui attribue un port temporaire, puis le client se connecte au port 3306 du serveur. Les ports sources sont donc différents de 3306, et différents d’un client à l’autre.

## Q8. Messages d’erreur obtenus. Où sont enregistrés les droits et qui les vérifie ? Conclusion pour la sécurité.
<img width="521" height="196" alt="image" src="https://github.com/user-attachments/assets/6fa93e13-608f-4c74-a43f-ae782a4491bf" />

Avec le compte étudiant (Windows), la commande UPDATE est refusée. Avec le compte secretariat (VM2), c’est la commande DELETE qui est refusée.

Messages d’erreur relevés : ERROR 1142 (42000) : UPDATE command denied to user ‘etudiant’@‘192.168.56.1’ for table ‘scolarite.note’ ; ERROR 1142 (42000) : DELETE command denied to user ‘secretariat’@‘192.168.56.12’ for table ‘scolarite.note’.

Les droits des comptes sont enregistrés dans les tables système de MariaDB, au niveau de la base de données, et c’est le serveur, et non le client, qui les vérifie. Le compte etudiant peut seulement lire, tandis que le compte secretariat peut saisir et lire. Chaque utilisateur ne peut donc effectuer que les opérations qui lui sont autorisées : la sécurité repose sur le contrôle exercé par le serveur.

## Q9. Le client Windows voit-il immédiatement la note modifiée depuis VM2 ?

Oui. Lorsque le client Windows envoie sa requête, le serveur lui renvoie les données actuelles. Les données étant centralisées à un seul endroit, tous les clients lisent la même version : c’est ce qui garantit la cohérence.

La centralisation des données garantit la cohérence car tous les clients accèdent à une base de données unique hébergée sur le serveur. Lorsqu’un client modifie une donnée, cette modification est enregistrée sur le serveur. Les autres clients récupèrent ensuite la valeur actualisée lorsqu’ils interrogent la base de données. Il n’est donc pas nécessaire de mettre à jour manuellement chaque machine.

## Q10. Identifiez la requête du client et la réponse du serveur dans la sortie de curl -v.

Le client se connecte au port 80 de VM1 ; le serveur accepte la connexion et répond. Dans la sortie de curl -v, les lignes précédées de > forment la requête du client, et celles précédées de < la réponse du serveur.

<img width="346" height="164" alt="image" src="https://github.com/user-attachments/assets/f150c42b-07c5-496d-bbe7-c0253d292544" />

* Requête : la première ligne (GET / HTTP/1.1) indique la méthode, la ressource demandée et la version du protocole. Les en-têtes précisent notamment le serveur visé (Host) et le logiciel client (User-Agent).
* Réponse : la première ligne (HTTP/1.1 200 OK) indique la version, le code de statut et son message. Les en-têtes précisent notamment le logiciel du serveur (Server) et le type du contenu (Content-Type).

## Q11. Quelles informations access.log enregistre-t-il sur chacun des deux clients ?
<img width="536" height="142" alt="image" src="https://github.com/user-attachments/assets/2f1cc6fb-b2a8-46b6-83f8-1335528c5374" />

Pour chaque client, le serveur enregistre :

* l’adresse IP du client ;
* la requête effectuée ;
* le code de statut HTTP ;
* la taille de la réponse ;
* le referer, c’est-à-dire la page d’origine de la requête ;
* le user agent : curl pour VM2 et Edge pour Windows.

## Q12. Comment le système sait-il à quel programme remettre un segment TCP ? Pourquoi le client doit-il connaître l’adresse ET le port ?

L’adresse IP désigne la machine, et le numéro de port de destination du segment TCP désigne le programme : le port 3306 est remis à MariaDB, le port 80 à Apache. Chaque serveur écoute sur son port, et le client doit connaître à l’avance l’adresse et le port pour pouvoir s’y connecter.

## Q13. Un avantage et un inconvénient d’une connexion persistante (MariaDB) et de requêtes indépendantes (HTTP). Comment un site web « se souvient-il » d’un utilisateur connecté ?

* MariaDB
    * Avantage : l’autorisation se fait une seule fois et plusieurs requêtes peuvent circuler sur la même connexion.
    * Inconvénient : la connexion et ses ressources sont maintenues côté serveur pendant toute la session, ce qui crée une forte dépendance au serveur.
* HTTP
    * Avantage : protocole léger, plus facile à utiliser et à mettre en place, avec des requêtes indépendantes.
    * Inconvénient : surcharge liée aux reconnexions.

Un site web « se souvient » d’un utilisateur connecté grâce à  une session (souvent associée à un cookie) ; après la connexion, le serveur crée une session identifiée par un identifiant unique, qu'il envoie au navigateur dans un cookie. À chaque requête suivante, le navigateur renvoie automatiquement ce cookie, ce qui permet au serveur de reconnaître l'utilisateur, car HTTP est un protocole sans état et ne retient rien par lui-même. 

## Q14. Message obtenu par chaque client, nombre de clients affectés, nom de ce défaut.
<img width="541" height="116" alt="image" src="https://github.com/user-attachments/assets/dfedac15-ba0b-4581-b459-d8dfdcd2c191" />

Lorsque le serveur est arrêté, le client Windows obtient le message Can’t connect to server on ‘192.168.56.11’ (10060), et le client VM2 le message ERROR 2002 (HY000): Can’t connect to server on ‘192.168.56.11’ (115).

Tous les clients sont affectés. Ce défaut d’architecture s’appelle le point unique de défaillance (single point of failure) : le serveur est un élément central, donc sa panne entraîne l’indisponibilité du service.

## Q15. Compte, requête et données dans la capture ; le mot de passe apparaît-il en clair ? Solution proposée.

La capture permet d’identifier l’adresse IP source et l’adresse IP destination des paquets, ainsi que le port 3306, qui est le port de MariaDB (MySQL).

Les paquets capturés entre 192.168.56.1 (port source 64598) et 192.168.56.11 (port 3306) sont des paquets MySQL : « Request Query » pour la requête envoyée par le client, « Response TABULAR » pour les données renvoyées par le serveur.

Le mot de passe n’apparaît pas en clair dans la capture.

Pour protéger les échanges, on utilise TLS/SSL, qui :

* chiffre les communications entre le client et le serveur ;
* empêche une personne qui intercepte les paquets de lire les données échangées ;
* protège les informations sensibles, notamment les requêtes SQL et leurs résultats.

## Q16. En une dizaine de lignes, définir le modèle client-serveur à partir des observations, puis citer deux avantages et deux inconvénients.

Le modèle client-serveur repose sur une séparation des rôles. Un programme, le serveur, reste en attente sur un port connu d’une machine connue, et les clients viennent s’y connecter quand ils ont besoin de lui. Dans notre TP, MariaDB et Apache tournaient sur VM1 et attendaient sur les ports 3306 et 80. C’est toujours le client qui prend l’initiative : Windows et VM2 ont ouvert chacun leur connexion, avec un port source choisi par leur système, puis ont envoyé leurs requêtes. Nous avons aussi vu que les données et les droits restent chez le serveur : tous les clients lisent la même version des données, et c’est MariaDB qui a refusé le UPDATE au compte etudiant et le DELETE au compte secretariat. Les clients ne communiquent jamais entre eux, ils passent toujours par le serveur.

Avantages. Les données sont centralisées, donc cohérentes : la note modifiée depuis VM2 est tout de suite apparue chez Windows. La gestion des droits est elle aussi centralisée, car l’administrateur contrôle les accès à un seul endroit.

Inconvénients. Le serveur est un point unique de défaillance : quand nous avons arrêté MariaDB, tous les clients ont perdu le service. Les échanges circulent en clair sur le réseau, comme l’a montré la capture tcpdump, ce qui oblige à ajouter un chiffrement comme TLS/SSL.
