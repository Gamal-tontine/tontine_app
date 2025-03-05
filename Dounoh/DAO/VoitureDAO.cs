using System;
using System.Linq;
using System.Windows.Forms;

namespace Dounoh.DAO
{
    class VoitureDAO
    {
        public bool Ajouter(string marque, string modele, string immatriculation, int chauffeurId, int place, string depart, string destination, string heureDepart)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    DateTime parsedHeureDepart;
                    if (!DateTime.TryParse(heureDepart, out parsedHeureDepart))
                    {
                        MessageBox.Show("Le format de l'heure de départ est incorrect.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }

                    Voiture nouvelleVoiture = new Voiture
                    {
                        marque = marque,
                        modele = modele,
                        immatriculation = immatriculation,
                        chauffeur_id = chauffeurId,
                        place = place,
                        depart = depart,
                        destination = destination,
                        heure_depart = parsedHeureDepart // Si la base de données attend un DateTime
                    };

                    db.Voiture.Add(nouvelleVoiture);
                    db.SaveChanges();
                    return true;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de l'ajout de la voiture : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }
        }

        public bool Modifier(int id, string marque, string modele, string immatriculation, int chauffeurId, int place, string depart, string destination, string heureDepart)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    DateTime parsedHeureDepart;
                    if (!DateTime.TryParse(heureDepart, out parsedHeureDepart))
                    {
                        MessageBox.Show("Le format de l'heure de départ est incorrect.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }

                    Voiture voiture = db.Voiture.SingleOrDefault(v => v.id == id);
                    if (voiture != null)
                    {
                        voiture.marque = marque;
                        voiture.modele = modele;
                        voiture.immatriculation = immatriculation;
                        voiture.chauffeur_id = chauffeurId;
                        voiture.place = place;
                        voiture.depart = depart;
                        voiture.destination = destination;
                        voiture.heure_depart = parsedHeureDepart; // Si la base de données attend un DateTime
                        db.SaveChanges();
                        return true;
                    }
                    else
                    {
                        MessageBox.Show("Voiture non trouvée.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de la modification : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }
        }

        public bool Supprimer(int id)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    Voiture voiture = db.Voiture.SingleOrDefault(v => v.id == id);
                    if (voiture != null)
                    {
                        db.Voiture.Remove(voiture);
                        db.SaveChanges();
                        return true;
                    }
                    else
                    {
                        MessageBox.Show("Voiture non trouvée.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de la suppression : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }
        }
    }
}