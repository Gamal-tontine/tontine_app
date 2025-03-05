using System;
using System.Data.Entity;
using System.Data.Entity.Infrastructure;

namespace Dounoh // Assurez-vous que l'espace de noms correspond à celui de votre projet
{
    public partial class GareRoutiereEntities : DbContext
    {
        public GareRoutiereEntities()
            : base("name=GareRoutiereEntities")
        {
        }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            throw new UnintentionalCodeFirstException();
        }

        public virtual DbSet<Chauffeur> Chauffeur { get; set; }
        public virtual DbSet<Passager> Passager { get; set; }
        public virtual DbSet<Voiture> Voiture { get; set; }
    }
}
