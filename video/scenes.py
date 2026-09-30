"""Scénario de la vidéo de démonstration (source unique pour la voix, la capture et le montage).

type = "carte" : image fixe générée ; type = "app" : séquence filmée dans l'outil.
Pour remplacer la voix de synthèse par la vôtre : déposez voix/<id>.perso.wav et relancez les 3 scripts.
"""

SCENES = [
    {
        "id": "01_intro", "type": "carte",
        "titre": "Quittance Tranquille",
        "sous": "Vos quittances de loyer,\nchaque mois en un clic.",
        "voix": "Voici Quittance Tranquille : vos quittances de loyer, chaque mois, en un seul clic.",
    },
    {
        "id": "02_donnees", "type": "carte",
        "titre": "Rien n'est envoyé\nsur un serveur",
        "sous": "Pas de compte. Pas de cloud.\nTout reste sur votre appareil.",
        "voix": "Pas de compte, pas de cloud : aucune donnée n'est envoyée sur un serveur. Tout reste sur votre téléphone ou votre ordinateur.",
    },
    {
        "id": "03_bail", "type": "app",
        "titre": "Le bail,\nune seule fois",
        "sous": "Bailleur, locataire, logement,\nloyer et charges.",
        "voix": "Renseignez le bail une seule fois : le bailleur, le locataire, le logement, puis le loyer et les charges.",
    },
    {
        "id": "04_agenda", "type": "app",
        "titre": "Vos rappels\ndans votre agenda",
        "sous": "Google Agenda, iPhone, Outlook.",
        "voix": "Choisissez vos rappels, et téléchargez le fichier agenda. Il s'ajoute à Google Agenda, à l'iPhone, ou à Outlook.",
    },
    {
        "id": "05_rappel", "type": "carte",
        "titre": "Chaque mois,\nl'agenda vous prévient",
        "sous": "Loyer bien reçu ?\nTouchez le lien du rappel.",
        "voix": "Chaque mois, le jour du loyer, votre agenda vous prévient. Le paiement est bien arrivé ? Touchez simplement le lien du rappel.",
    },
    {
        "id": "06_quittance", "type": "app",
        "titre": "La quittance\ndéjà remplie",
        "sous": "Période et dates\ncalculées pour vous.",
        "voix": "La quittance du mois s'ouvre, déjà remplie. La période et les dates sont calculées automatiquement.",
    },
    {
        "id": "07_recu", "type": "app",
        "titre": "Paiement partiel ?\nUn reçu.",
        "sous": "Le reste dû est\ncalculé tout seul.",
        "voix": "Le loyer n'est payé qu'en partie ? Un geste, et la quittance devient un reçu, avec le reste dû.",
    },
    {
        "id": "08_envoi", "type": "app",
        "titre": "Le PDF,\nprêt à envoyer",
        "sous": "Par e-mail ou messagerie,\nc'est vous qui l'envoyez.",
        "voix": "Téléchargez le PDF, ou partagez-le au locataire, par e-mail ou par messagerie. C'est toujours vous qui l'envoyez.",
    },
    {
        "id": "09_outro", "type": "carte",
        "titre": "Quittance Tranquille",
        "sous": "Gratuit. Sans compte.\nAucune donnée envoyée sur un serveur.",
        "voix": "Quittance Tranquille. C'est gratuit, sans compte, et aucune donnée n'est envoyée sur un serveur.",
    },
]

# Marge de silence après chaque phrase (secondes)
MARGE = 0.6
