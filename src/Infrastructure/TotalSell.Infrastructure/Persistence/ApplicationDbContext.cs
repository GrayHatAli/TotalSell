using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Domain.Entities;

namespace TotalSell.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<ReportCategory> ReportCategories { get; set; }
    public DbSet<Report> Reports { get; set; }
    public DbSet<ReportDashboard> ReportDashboards { get; set; }
    public DbSet<ReportDashboardItem> ReportDashboardItems { get; set; }
    public DbSet<ReportDashboardVersion> ReportDashboardVersions => Set<ReportDashboardVersion>();
    public DbSet<ReportVersion> ReportVersions { get; set; }
    public DbSet<ReportView> ReportViews { get; set; }
    public DbSet<ReportFavorite> ReportFavorites { get; set; }
    public DbSet<ReportComment> ReportComments { get; set; }
    public DbSet<ReportPermission> ReportPermissions { get; set; }
    public DbSet<ReportExecution> ReportExecutions { get; set; }
    public DbSet<ReportAudit> ReportAudits { get; set; }
    public DbSet<ReportDashboardAudit> ReportDashboardAudits { get; set; }
    public DbSet<ReportDashboardFavorite> ReportDashboardFavorites { get; set; }
    public DbSet<ReportDashboardSchedule> ReportDashboardSchedules { get; set; }
    public DbSet<ReportSubscription> ReportSubscriptions { get; set; }
    public DbSet<ReportDashboardSubscription> ReportDashboardSubscriptions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
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