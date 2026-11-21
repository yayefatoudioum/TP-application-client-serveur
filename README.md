# TP1 – Le modèle client-serveur
## Présentation
Ce dépôt contient le compte rendu du TP1 réalisé dans le cadre du module Applications Client-Serveur et Web (ACSW)
Ce TP a pour objectif de mettre en pratique le modèle client-serveur à travers l'installation et la configuration de MariaDB et Apache sur une machine virtuelle Linux.

## Objectifs du TP

- Installer et configurer un serveur MariaDB.
- Installer et configurer un serveur Web Apache.
- Configurer les adresses IP des machines et assurer leur communication.
- Permettre aux clients Windows et Linux d'accéder aux services du serveur.
- Étudier les connexions simultanées de plusieurs clients.
- Comprendre la gestion des utilisateurs et des droits d'accès.
- Analyser les échanges réseau avec Wireshark et tcpdump.
- Identifier les limites et les problèmes de sécurité du modèle client-serveur.

## Architecture utilisée

Le TP repose sur trois machines connectées à un réseau privé :

| Machine | Adresse IP | Rôle |

| Windows | 192.168.56.1 | Client 1 |

| VM1 Linux | 192.168.56.11 | Serveur MariaDB et Apache |

| VM2 Linux | 192.168.56.12 | Client 2 |

## Travail réalisé

### 1. Configuration du serveur MariaDB
Installation du serveur, création de la base de données `scolarite` et réalisation de requêtes SQL.

### 2. Ouverture du service au réseau
Configuration de l'adresse d'écoute du serveur et création des comptes utilisateurs pour les connexions distantes.

### 3. Connexions de plusieurs clients
Test des connexions simultanées depuis Windows et VM2, avec observation des droits et des échanges.

### 4. Mise en place du serveur Web
Installation d'Apache et consultation d'une page Web depuis les deux clients à l'aide de HTTP.

### 5. Étude des limites du modèle
Observation des conséquences de l'arrêt du serveur et analyse du trafic réseau avec tcpdump.

## Conclusion

Ce TP nous a permis de comprendre le fonctionnement du modèle client-serveur, la centralisation des données, la gestion des droits d'accès et la communication entre plusieurs machines.
Nous avons également constaté ses limites, notamment le point unique de défaillance et les risques liés aux échanges non chiffrés.

## Etudiantes

- Yaye Fatou Niang Dioum
- Fatoumata Bintou Capho Diouf

## Encadrant

Dr Keba Gueye

**Année académique : 2026–2027**
