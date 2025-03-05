using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace Dounoh.DAO
{
    class ChauffeurDAO
    {
        public bool Ajouter(string prenom, string nom, string adresse, string telephone)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    Chauffeur nouveauChauffeur = new Chauffeur
                    {
                        prenom = prenom,
                        nom = nom,
                        adresse = adresse,
                        telephone = telephone
                    };

                    db.Chauffeur.Add(nouveauChauffeur);
                    db.SaveChanges();
                    return true;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de l'ajout du chauffeur : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }
        }

        public bool Modifier(int id, string prenom, string nom, string adresse, string telephone)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    Chauffeur chauffeur = db.Chauffeur.SingleOrDefault(c => c.id == id);
                    if (chauffeur != null)
                    {
                        chauffeur.prenom = prenom;
                        chauffeur.nom = nom;
                        chauffeur.adresse = adresse;
                        chauffeur.telephone = telephone;
                        db.SaveChanges();
                        return true;
                    }
                    else
                    {
                        MessageBox.Show("Chauffeur non trouvé.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
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
                    Chauffeur chauffeur = db.Chauffeur.SingleOrDefault(c => c.id == id);
                    if (chauffeur != null)
                    {
                        db.Chauffeur.Remove(chauffeur);
                        db.SaveChanges();
                        return true;
                    }
                    else
                    {
                        MessageBox.Show("Chauffeur non trouvé.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
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

        public Chauffeur ObtenirChauffeur(int id)
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    Chauffeur chauffeur = db.Chauffeur.SingleOrDefault(c => c.id == id);
                    if (chauffeur != null)
                    {
                        return chauffeur;
                    }
                    else
                    {
                        MessageBox.Show("Chauffeur non trouvé.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return null;
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de la récupération des informations : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return null;
                }
            }
        }

        public List<Chauffeur> ObtenirTousLesChauffeurs()
        {
            using (GareRoutiereEntities db = new GareRoutiereEntities())
            {
                try
                {
                    return db.Chauffeur.ToList();
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Erreur lors de la récupération de la liste des chauffeurs : " + ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return new List<Chauffeur>();
                }
            }
        }
    }
}
