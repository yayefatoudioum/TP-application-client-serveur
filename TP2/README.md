## Étudiantes

- Yaye Fatou Niang Dioum
- Fatoumata Bintou Capho Diouf

## Encadrant

Dr Keba Gueye

**Année académique : 2026–2027**

## TP 2 – ARCHITECTURES 2-TIERS ET 3-TIERS : ***réponses aux questions***

## Q1. Relevez dans le code les lignes qui relèvent de la présentation, celles qui relèvent de la logique métier, et celles qui relèvent de l’accès aux données. Sur quelle machine s’exécutent-elles toutes ?

* **Présentation :** lignes **96 à 113** (menu et affichage), plus les lignes d’affichage placées dans les fonctions de relevé et de classement : 53-54, 61-63, 69, 73, 85, 91, 93.
* **Logique métier :** 28-30 (validation de la note sur 10 et pondération par les crédits) ; 39-42 (calcul de la moyenne) ; 71-72 (décision Validé / Non validé) ; 85-88 et 92 (tri du classement, regroupement des notes par étudiant, comptage des admis).
* **Accès aux données :** 22-26 (adresse du serveur, compte, mot de passe) ; 33-36 (fonction connexion ()) ; requêtes SQL en 47-48, 52-53, 58-59, 64-66 et 80-82 ; 45-48 (octets reçus ()).
* **Les trois couches s'exécutent sur la machine client (Windows ou VM2)** 
## Q2. Quelles informations un étudiant qui récupère client_lourd.py obtient-il sur le serveur de base de données ? Que peut-il faire avec, en dehors du programme ?

Il obtient l’adresse du serveur MariaDB (VM1, 192.168.56.11, port 3306), le nom d’utilisateur et le mot de passe en clair (etudiant / Etudiant@2026), le nom de la base (scolarite), ainsi que la structure des données (tables, colonnes) et les règles métier, lisibles dans le code.

En dehors du programme, il peut se connecter directement à la base avec le compte **étudiant** et lire les notes de tous les étudiants, pas seulement les siennes.

## Q3. Qu’aurait-il fallu installer sur les 300 postes d’une salle informatique pour déployer cette application ?

Sur chacun des 300 postes il aurait fallu installer **Python 3**, la bibliothèque **pymysql** (py -m pip install pymysql) et le fichier **client_lourd.py**.

## Q4. Les deux architectures donnent-elles la même moyenne pour ESP260001 et le même nombre d’admis ? Pourquoi est-ce indispensable pour cette expérience ?

Oui, elles donnent la même moyenne pour **ESP260001 et le même nombre d’admis**.

C’est indispensable pour comparer les deux architectures **à fonctionnalité égale** : les deux versions utilisent les mêmes données (même base scolarite) et les mêmes règles (même formule de moyenne, même seuil de validation). Donc, avec des résultats identiques, on sait que **l’écart vient de l’architecture et on peut attribuer à elle seule les différences observées ailleurs**.

***2-Tiers:***


<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/2dd09954-bd62-4175-8c68-0f76be18ce30" />


***3-Tiers:***

<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/dffec65f-7fdd-4a71-82c9-cf811ada9d3f" />
<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/de63ae6c-577d-47de-977b-5a58da0274d1" />








## Q5. Qu’a dû installer le poste Windows pour utiliser la version 3-tiers ? Comparez avec Q3.

**Rien**, un navigateur web suffit (Edge, Chrome, etc.).

Par comparaison avec Q3, il n’y a plus de Python, de pymysql ni de programme à installer sur 300 postes. Les installations (Apache, PHP, php-mysql) sont faites **une seule fois**, sur VM2.

**Le modèle 3-tiers est donc plus léger côté client et plus simple à déployer.**

## Q6. Que renvoie la requête vers config.php ? Expliquez pourquoi le mot de passe n’est jamais envoyé au navigateur.


<img width="511" height="87" alt="image" src="https://github.com/user-attachments/assets/303e6ced-4008-4805-8120-a749b639c70b" />

La requête curl.exe -i http://192.168.56.12/scolarite/inc/config.php renvoie un code **HTTP 200** avec un **corps vide** (ou quasi vide). On ne voit pas le contenu du fichier.

Apache ne renvoie pas le fichier, il le confie à l’interpréteur PHP qui l’**exécute côté serveur**. **config.php** ne fait que définir des variables (adresse, compte, mot de passe) et n’affiche rien : le résultat de l’exécution est donc vide. Le mot de passe reste dans la mémoire du serveur d’application et n’est utilisé que pour se connecter à MariaDB.

## Q7. Le compte app_scolarite n’est autorisé que depuis 192.168.56.12. Combien de comptes MariaDB faut-il en 3-tiers, quel que soit le nombre d’utilisateurs ? Et en 2-tiers ?

**En 3-tiers :** un seul compte (app_scolarite), utilisé par le serveur d’application, quel que soit le nombre d’utilisateurs.

**En 2-tiers :** autant de comptes que d’utilisateurs (si l’on veut les distinguer), ou un compte partagé par tous, ce qui est dangereux (voir réponse Q2).

## Q8. Ouvrez le code source de la page dans le navigateur (Ctrl+U). Y trouvez-vous une trace de SQL ou de la règle de calcul ? Qu’est-ce que le navigateur reçoit exactement ?

<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/69b332cb-c6f3-472c-ab52-257f30a3eb92" />

<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/eb015acd-4b4f-4479-9351-21a7adbe1422" />





**Non**, on n’y trouve aucune trace de SQL ni de la règle de calcul. Le navigateur reçoit uniquement le **code HTML** (éventuellement CSS) de la page affichée : le résultat du calcul et non la façon dont il a été obtenu.

## Q9. Relevez la décision pour ESP260011 et le nombre d’admis sur chaque poste en 2-tiers. Que constatez-vous ? Quelles conséquences réelles cela aurait-il pour un service de scolarité ?

<!-- Insérer ici les captures du relevé de ESP260011 sur Windows (v1.0) et sur VM2 (v1.1) -->

Les deux postes donnent des résultats différents :

* **En v1.0 :** ESP260011 est « **Validé** » et le nombre d’admis est de **18 étudiants**.

  <img width="296" height="149" alt="image" src="https://github.com/user-attachments/assets/fcd04827-0c46-490d-a70d-17e0d5fef6b0" />

* **En v1.1 :** ESP260011 est « **Non validé** » avec une note de 7.50 en mathématiques discrètes, et le nombre d’admis est plus faible, passant de **18 à 16 étudiants**.

  <img width="320" height="109" alt="image" src="https://github.com/user-attachments/assets/c00f03f2-2086-4f06-8450-3f909ae273f3" />


Nous constatons donc que, pour **les mêmes données**, deux utilisateurs obtiennent des décisions contradictoires, selon **la version de leur poste**.

Comme **conséquences réelles**, on a un étudiant déclaré admis par un poste et refusé par un autre, des contestations de résultats, des PV de jury non fiables, une perte de confiance dans le service de scolarité et un risque juridique.

## Q10. Combien de fichiers et de machines avez-vous modifiés en 3-tiers ? Combien d’utilisateurs ont bénéficié de la nouvelle règle, et à quel moment ?

**Un seul fichier** (metier.php) sur **une seule machine** (VM2).

**Tous les utilisateurs**, Windows comme VM2, ont bénéficié de la nouvelle règle **immédiatement**, dès le rechargement de la page suivante, sans rien installer de leur côté.

## Q11. Dans metier.php, la moyenne est calculée par le SGBD (SUM(...)/SUM(...)), alors que client_lourd.py la calcule en Python. Où avez-vous dû intervenir pour la règle éliminatoire dans chaque cas ?

* **En 2-tiers :** on a modifié le code Python de client_lourd.py, à deux endroits : la fonction du relevé (décision) et le décompte des admis (classement), plus la constante NOTE_ELIMINATOIRE et VERSION = "1.1".

  <img width="392" height="221" alt="image" src="https://github.com/user-attachments/assets/fb6bc2e7-e503-4ce6-b780-1607f4e5f20a" />


* **En 3-tiers :** dans metier.php, on a changé le code du relevé (décision) et du classement (admis), plus la constante et VERSION_APPLI = '1.1'. La moyenne, déjà calculée par SQL, n’a pas eu à changer.

<img width="355" height="154" alt="image" src="https://github.com/user-attachments/assets/1f2bbdde-86ae-4d80-a277-eb4e006c5cc2" />
<img width="355" height="154" alt="image" src="https://github.com/user-attachments/assets/bdbc52c0-8cd8-425a-b159-6080b26f889c" />
<img width="355" height="154" alt="image" src="https://github.com/user-attachments/assets/e07da429-0e8a-45b0-8ad3-766b8bc9fa08" />



## Q12. Complétez le tableau. D’où vient l’écart de volume ? Que deviendrait-il pour 300 postes reliés par une liaison à 10 Mbit/s, ou pour un client sur une connexion mobile ?

<img width="100" height="10" alt="image" src="https://github.com/user-attachments/assets/44aced74-7ebd-437b-9ea4-b75110d5628c" />
<img width="412" height="19" alt="image" src="https://github.com/user-attachments/assets/2f2d85fd-621d-47f7-9987-7c371fc3275f" />


**Tableau des mesures :**

| Mesure | 2-tiers | 3-tiers |
|---|---|---|
| Lignes ou octets reçus par le poste client | 120180 lignes ou 2407.3 Kio | 10 lignes |
| Temps de calcul du classement | 719 ms | 722 ms |
| Machine qui a effectué le calcul | Le poste client Windows | Le serveur d’application (VM2) et le SGBD (VM1) |

En 2-tiers, le client reçoit des dizaines de milliers de lignes (les notes brutes, jusqu’à 120 000) et calcule lui-même ; en 3-tiers, il ne reçoit qu’une page HTML de quelques ko, car le calcul est fait sur VM2 / dans MariaDB.

L’écart vient de l’endroit où le calcul est fait : en 2-tiers, il faut ramener toutes les données au client pour calculer ; en 3-tiers, on ne transporte que le résultat.

À 10 Mbit/s avec 300 postes, ou sur connexion mobile, le trafic 2-tiers deviendrait un goulot d’étranglement (lenteur, saturation de la liaison, coût en data) alors que le 3-tiers resterait léger.

## Q13. Le client lourd lit la valeur Bytes_sent du serveur avant et après la requête : que mesure exactement cette valeur ? Pourquoi est-ce une mesure honnête du trafic ?

**Bytes_sent** est un compteur de MariaDB : le nombre d’octets que le serveur a envoyés au client. La différence entre la valeur après et la valeur avant la requête donne le volume de données renvoyé pour cette requête.

C’est une mesure honnête car elle est faite par le serveur lui-même, côté émission, donc indépendante de ce que le programme client prétend ou de la manière dont il stocke les données.

## Q14. Que se passe-t-il pour chaque architecture ? Pourquoi ne peut-on pas appliquer cette protection en 2-tiers ?


* **Architecture 2-tiers :** client_lourd.py sur Windows ne parvient plus à se connecter (erreur de connexion / délai dépassé), car le pare-feu de VM1 n’autorise le port 3306 que depuis 192.168.56.12.

  <img width="707" height="56" alt="image" src="https://github.com/user-attachments/assets/937005f5-f664-4e18-89dc-9439a598c181" />

* **Architecture 3-tiers :** l’application web continue de fonctionner, car c’est VM2 (autorisée) qui parle à la base, pas le poste de l’utilisateur.

  <img width="322" height="139" alt="image" src="https://github.com/user-attachments/assets/37ce58b5-fd9b-412a-ba2c-545f75b6ab6d" />


**Pourquoi pas cette protection en 2-tiers ?** C’est parce que les clients sont les postes des utilisateurs : si on les bloque, l’application ne marche plus pour eux. Il faudrait ouvrir 3306 à tous les postes (300 adresses, parfois variables, voire Internet), c’est-à-dire exposer la base.

## Q15. Citez deux autres risques de sécurité propres au client lourd, et la façon dont le 3-tiers les supprime ou les réduit.

**Risque 1 : le code et les identifiants sont chez l’utilisateur.** Le programme peut être lu, décompilé ou copié, et révèle les identifiants. En 3-tiers, le code et les identifiants restent sur le serveur et n’atteignent jamais le navigateur (voir réponse Q6).

**Risque 2 : le programme peut être modifié ou contourné.** Un utilisateur malveillant peut changer le code (par exemple pour afficher les notes d’un autre étudiant ou truquer une règle) ou envoyer ses propres requêtes SQL avec le compte de la base. En 3-tiers, le serveur ne propose que les opérations prévues par l’application et applique lui-même les contrôles : **l’utilisateur ne touche jamais au SQL.**

## Q16. Le 2-tiers reste utilisé : logiciel de caisse d’une boutique, poste de saisie d’un laboratoire, outil d’administration d’une base. Donnez les conditions qui le rendent acceptable, puis justifiez le choix du 3-tiers pour un service de scolarité utilisé par toute l’université.

**Le 2-tiers est acceptable quand** le nombre de postes est petit et connu ; les utilisateurs sont de confiance (personnel interne) ; le réseau est local et fiable ; les volumes échangés sont modestes ; les règles évoluent peu ; le développement doit rester simple et peu coûteux.

**Le 3-tiers s’impose pour la scolarité** car on y trouve des milliers d’utilisateurs (étudiants, enseignants, administration) sur des postes très variés, dont certains non maîtrisés ; des règles de gestion qui évoluent (comme la règle de la v1.1) et doivent être identiques pour tous ; des données sensibles (notes) à protéger derrière un point d’accès unique ; un accès possible depuis l’extérieur (mobile, domicile) qui rend le trafic et la sécurité critiques.
