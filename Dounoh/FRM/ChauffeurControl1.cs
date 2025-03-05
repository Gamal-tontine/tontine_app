using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using Dounoh.DAO;

namespace Dounoh.FRM
{
    public partial class ChauffeurControl1 : UserControl
    {
        private static ChauffeurControl1 chauffeur;
        public static ChauffeurControl1 Instance
        {
            get
            {
                if (chauffeur == null)
                {
                    chauffeur = new ChauffeurControl1();
                }
                return chauffeur;
            }
        }

        public ChauffeurControl1()
        {
            InitializeComponent();
            buttonSave.Click += ButtonSave_Click;
            buttonUpdate.Click += ButtonUpdate_Click;
            buttonDelete.Click += ButtonDelete_Click;
        }

        private void InitializeComponent()
        {
            this.textBoxPrenom = new TextBox();
            this.textBoxNom = new TextBox();
            this.textBoxAdresse = new TextBox();
            this.textBoxTelephone = new TextBox();
            this.labelPrenom = new Label();
            this.labelNom = new Label();
            this.labelAdresse = new Label();
            this.labelTelephone = new Label();
            this.buttonSave = new Button();
            this.buttonUpdate = new Button();
            this.buttonDelete = new Button();

            this.SuspendLayout();

            // 
            // textBoxPrenom
            // 
            this.textBoxPrenom.Location = new Point(100, 20);
            this.textBoxPrenom.Name = "textBoxPrenom";
            this.textBoxPrenom.Size = new Size(200, 20);

            // 
            // textBoxNom
            // 
            this.textBoxNom.Location = new Point(100, 60);
            this.textBoxNom.Name = "textBoxNom";
            this.textBoxNom.Size = new Size(200, 20);

            // 
            // textBoxAdresse
            // 
            this.textBoxAdresse.Location = new Point(100, 100);
            this.textBoxAdresse.Name = "textBoxAdresse";
            this.textBoxAdresse.Size = new Size(200, 20);

            // 
            // textBoxTelephone
            // 
            this.textBoxTelephone.Location = new Point(100, 140);
            this.textBoxTelephone.Name = "textBoxTelephone";
            this.textBoxTelephone.Size = new Size(200, 20);

            // 
            // labelPrenom
            // 
            this.labelPrenom.Location = new Point(20, 20);
            this.labelPrenom.Name = "labelPrenom";
            this.labelPrenom.Size = new Size(80, 20);
            this.labelPrenom.Text = "Prénom:";

            // 
            // labelNom
            // 
            this.labelNom.Location = new Point(20, 60);
            this.labelNom.Name = "labelNom";
            this.labelNom.Size = new Size(80, 20);
            this.labelNom.Text = "Nom:";

            // 
            // labelAdresse
            // 
            this.labelAdresse.Location = new Point(20, 100);
            this.labelAdresse.Name = "labelAdresse";
            this.labelAdresse.Size = new Size(80, 20);
            this.labelAdresse.Text = "Adresse:";

            // 
            // labelTelephone
            // 
            this.labelTelephone.Location = new Point(20, 140);
            this.labelTelephone.Name = "labelTelephone";
            this.labelTelephone.Size = new Size(80, 20);
            this.labelTelephone.Text = "Téléphone:";

            // 
            // buttonSave
            // 
            this.buttonSave.Location = new Point(20, 180);
            this.buttonSave.Name = "buttonSave";
            this.buttonSave.Size = new Size(80, 30);
            this.buttonSave.Text = "Enregistrer";

            // 
            // buttonUpdate
            // 
            this.buttonUpdate.Location = new Point(120, 180);
            this.buttonUpdate.Name = "buttonUpdate";
            this.buttonUpdate.Size = new Size(80, 30);
            this.buttonUpdate.Text = "Modifier";

            // 
            // buttonDelete
            // 
            this.buttonDelete.Location = new Point(220, 180);
            this.buttonDelete.Name = "buttonDelete";
            this.buttonDelete.Size = new Size(80, 30);
            this.buttonDelete.Text = "Supprimer";

            // 
            // ChauffeurControl1
            // 
            this.Controls.Add(this.textBoxPrenom);
            this.Controls.Add(this.textBoxNom);
            this.Controls.Add(this.textBoxAdresse);
            this.Controls.Add(this.textBoxTelephone);
            this.Controls.Add(this.labelPrenom);
            this.Controls.Add(this.labelNom);
            this.Controls.Add(this.labelAdresse);
            this.Controls.Add(this.labelTelephone);
            this.Controls.Add(this.buttonSave);
            this.Controls.Add(this.buttonUpdate);
            this.Controls.Add(this.buttonDelete);
            this.Name = "ChauffeurControl1";
            this.Size = new Size(320, 230);
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private void ButtonSave_Click(object sender, EventArgs e)
        {
            ChauffeurDAO chauffeurDAO = new ChauffeurDAO();
            bool success = chauffeurDAO.Ajouter(textBoxPrenom.Text, textBoxNom.Text, textBoxAdresse.Text, textBoxTelephone.Text);
            if (success)
            {
                MessageBox.Show("Chauffeur enregistré avec succès!", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void ButtonUpdate_Click(object sender, EventArgs e)
        {
            ChauffeurDAO chauffeurDAO = new ChauffeurDAO();
            // Assurez-vous d'utiliser l'ID approprié pour la modification
            bool success = chauffeurDAO.Modifier(/*ID à modifier*/, textBoxPrenom.Text, textBoxNom.Text, textBoxAdresse.Text, textBoxTelephone.Text);
            if (success)
            {
                MessageBox.Show("Chauffeur modifié avec succès!", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void ButtonDelete_Click(object sender, EventArgs e)
        {
            ChauffeurDAO chauffeurDAO = new ChauffeurDAO();
            // Assurez-vous d'utiliser l'ID approprié pour la suppression
            bool success = chauffeurDAO.Supprimer(/*ID à supprimer*/);
            if (success)
            {
                MessageBox.Show("Chauffeur supprimé avec succès!", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private TextBox textBoxPrenom;
        private TextBox textBoxNom;
        private TextBox textBoxAdresse;
        private TextBox textBoxTelephone;
        private Label labelPrenom;
        private Label labelNom;
        private Label labelAdresse;
        private Label labelTelephone;
        private Button buttonSave;
        private Button buttonUpdate;
        private Button buttonDelete;
    }
}
