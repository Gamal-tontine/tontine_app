using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Dounoh.FRM
{
    public partial class Principale : Form
    {
        public Principale()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            pnlBarre.Top = bntpassager.Top;

            if (!pnlAfficher.Controls.Contains(Passager.Instance))
            {
                pnlAfficher.Controls.Clear();
                pnlAfficher.Controls.Add(Passager.Instance);
                Passager.Instance.Dock = DockStyle.Fill;
                Passager.Instance.BringToFront();
            }
            else
            {
                Passager.Instance.BringToFront();
            }
        }

        private void btnvoiture_Click(object sender, EventArgs e)
        {
            pnlBarre.Top = btnvoiture.Top;

            if (!pnlAfficher.Controls.Contains(VoitureControl.Instance))
            {
                pnlAfficher.Controls.Clear(); 
                pnlAfficher.Controls.Add(VoitureControl.Instance);
                VoitureControl.Instance.Dock = DockStyle.Fill;
                VoitureControl.Instance.BringToFront();
            }
            else
            {
                VoitureControl.Instance.BringToFront();
            }
        }

        private void bntchauffeur_Click(object sender, EventArgs e)
        {
            pnlBarre.Top = btnchauffeur.Top;

            if (!pnlAfficher.Controls.Contains(ChauffeurControl1.Instance))
            {
                pnlAfficher.Controls.Clear();
                pnlAfficher.Controls.Add(ChauffeurControl1.Instance);
                ChauffeurControl1.Instance.Dock = DockStyle.Fill;
                ChauffeurControl1.Instance.BringToFront();
            }
            else
            {
                ChauffeurControl1.Instance.BringToFront();
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Principale_Load(object sender, EventArgs e)
        {

        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void btnvoiture_Click_1(object sender, EventArgs e)
        {
            pnlBarre.Top = btnvoiture.Top;

            if (!pnlAfficher.Controls.Contains(VoitureControl.Instance))
            {
                pnlAfficher.Controls.Clear();
                pnlAfficher.Controls.Add(VoitureControl.Instance);
                VoitureControl.Instance.Dock = DockStyle.Fill;
                VoitureControl.Instance.BringToFront();
            }
            else
            {
                VoitureControl.Instance.BringToFront();
            }
        }
    }
}