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

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Invoice> Invoices => Set<Invoice>();
    public DbSet<ReportCategory> ReportCategories => Set<ReportCategory>();
    public DbSet<Report> Reports => Set<Report>();
    public DbSet<ReportDashboard> ReportDashboards => Set<ReportDashboard>();
    public DbSet<ReportDashboardItem> ReportDashboardItems => Set<ReportDashboardItem>();
    public DbSet<ReportDashboardVersion> ReportDashboardVersions => Set<ReportDashboardVersion>();
    public DbSet<ReportVersion> ReportVersions => Set<ReportVersion>();
    public DbSet<ReportView> ReportViews => Set<ReportView>();
    public DbSet<ReportFavorite> ReportFavorites => Set<ReportFavorite>();
    public DbSet<ReportComment> ReportComments => Set<ReportComment>();
    public DbSet<ReportPermission> ReportPermissions => Set<ReportPermission>();
    public DbSet<ReportExecution> ReportExecutions => Set<ReportExecution>();
    public DbSet<ReportAudit> ReportAudits => Set<ReportAudit>();
    public DbSet<ReportDashboardAudit> ReportDashboardAudits => Set<ReportDashboardAudit>();
    public DbSet<ReportDashboardFavorite> ReportDashboardFavorites => Set<ReportDashboardFavorite>();
    public DbSet<ReportDashboardSchedule> ReportDashboardSchedules => Set<ReportDashboardSchedule>();
    public DbSet<ReportSubscription> ReportSubscriptions => Set<ReportSubscription>();
    public DbSet<ReportDashboardSubscription> ReportDashboardSubscriptions => Set<ReportDashboardSubscription>();

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