using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence;

public class ApplicationDbContext : Application.Common.Persistence.ApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<Application.Common.Persistence.ApplicationDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        modelBuilder.Entity<ReportDashboardVersion>(entity =>
        {
            entity.ToTable("ReportDashboardVersions");
            
            entity.Property(e => e.Version)
                .IsRequired()
                .HasMaxLength(50);
                
            entity.Property(e => e.Description)
                .HasMaxLength(500);
                
            entity.Property(e => e.Layout)
                .HasMaxLength(1000);
                
            entity.Property(e => e.Theme)
                .HasMaxLength(100);
                
            entity.Property(e => e.Parameters)
                .HasMaxLength(1000);
                
            entity.Property(e => e.Filters)
                .HasMaxLength(1000);
                
            entity.Property(e => e.Status)
                .HasMaxLength(50);
                
            entity.Property(e => e.ApprovedBy)
                .HasMaxLength(100);
                
            entity.Property(e => e.RejectedBy)
                .HasMaxLength(100);
                
            entity.Property(e => e.RejectionReason)
                .HasMaxLength(500);
                
            entity.HasIndex(e => e.DashboardId);
            entity.HasIndex(e => e.Status);
            entity.HasIndex(e => e.Version);
        });
    }
} 