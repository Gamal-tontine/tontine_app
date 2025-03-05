using System;
using System.Windows.Forms;
using Dounoh.DAO;

namespace Dounoh.FRM
{
    public partial class VoitureControl : UserControl
    {
        private static VoitureControl _instance;
        public static VoitureControl Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = new VoitureControl();
                }
                return _instance;
            }
        }

        private VoitureDAO voitureDAO;

        public VoitureControl()
        {
            InitializeComponent();
            voitureDAO = new VoitureDAO();
        }

        private void buttonSave_Click(object sender, EventArgs e)
        {
            // Validation des entrées
            if (string.IsNullOrEmpty(textBoxMarque.Text) || string.IsNullOrEmpty(textBoxModele.Text))
            {
                MessageBox.Show("Veuillez remplir tous les champs obligatoires.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (!int.TryParse(textBoxChauffeur.Text, out int chauffeurId))
            {
                MessageBox.Show("L'ID du chauffeur doit être un nombre entier.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (!int.TryParse(textBoxPlace.Text, out int place))
            {
                MessageBox.Show("Le nombre de places doit être un nombre entier.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Appeler la méthode Ajouter
            bool success = voitureDAO.Ajouter(
                textBoxMarque.Text,
                textBoxModele.Text,
                textBoxImmatriculation.Text,
                chauffeurId,
                place,
                textBoxDepart.Text,
                textBoxDestination.Text,
                textBoxHeureDepart.Text
            );

            if (success)
            {
                MessageBox.Show("Voiture ajoutée avec succès", "Sauvegarde", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("Une voiture avec cette immatriculation existe déjà", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void buttonUpdate_Click(object sender, EventArgs e)
        {
            int selectedCarId = GetSelectedCarId();
            if (selectedCarId == -1)
            {
                return; // Aucune voiture sélectionnée
            }

            bool success = voitureDAO.Modifier(
                selectedCarId,
                textBoxMarque.Text,
                textBoxModele.Text,
                textBoxImmatriculation.Text,
                int.Parse(textBoxChauffeur.Text),
                int.Parse(textBoxPlace.Text),
                textBoxDepart.Text,
                textBoxDestination.Text,
                textBoxHeureDepart.Text
            );

            if (success)
            {
                MessageBox.Show("Voiture mise à jour avec succès", "Modification", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("Erreur lors de la mise à jour de la voiture", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            int selectedCarId = GetSelectedCarId();
            if (selectedCarId == -1)
            {
                return; // Aucune voiture sélectionnée
            }

            bool success = voitureDAO.Supprimer(selectedCarId);
            if (success)
            {
                MessageBox.Show("Voiture supprimée avec succès", "Suppression", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("Erreur lors de la suppression de la voiture", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private int GetSelectedCarId()
        {
            // Implémentez cette méthode pour retourner l'ID de la voiture sélectionnée
            // Exemple avec une DataGridView :
            if (dataGridViewVoitures.SelectedRows.Count > 0)
            {
                return (int)dataGridViewVoitures.SelectedRows[0].Cells["id"].Value;
            }
            else
            {
                MessageBox.Show("Veuillez sélectionner une voiture.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return -1; // Retourner une valeur invalide si rien n'est sélectionné
            }
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            // Code pour gérer l'événement textChanged pour textBox2
        }
    }
}