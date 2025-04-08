using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Common.Persistence;

public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Invoice> Invoices { get; set; }
    public DbSet<InvoiceItem> InvoiceItems { get; set; }
    public DbSet<Customer> Customers { get; set; }
    public DbSet<Product> Products { get; set; }
    public DbSet<ReportCategory> ReportCategories { get; set; }
    public DbSet<Report> Reports { get; set; }
    public DbSet<ReportDashboard> ReportDashboards { get; set; }
    public DbSet<ReportDashboardItem> ReportDashboardItems { get; set; }
    public DbSet<ReportDashboardVersion> ReportDashboardVersions { get; set; }
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
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
} 