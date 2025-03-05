using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Dounoh.FRM
{
    public partial class Passager : UserControl
    {

        private static Passager passager;

        public static Passager Instance
        {
            get
            {
                if (passager == null)
                {
                    passager = new Passager();

                }
                return passager;
            }
        }

        public Passager()
        {
            InitializeComponent();
        }

        private void label16_Click(object sender, EventArgs e)
        {

        }
    }
}
