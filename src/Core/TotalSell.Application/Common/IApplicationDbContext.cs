using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Common;

public interface IApplicationDbContext
{
    DbSet<Customer> Customers { get; }
    DbSet<Product> Products { get; }
    DbSet<Invoice> Invoices { get; }
    DbSet<ReportCategory> ReportCategories { get; }
    DbSet<Report> Reports { get; }
    DbSet<ReportDashboard> ReportDashboards { get; }
    DbSet<ReportDashboardItem> ReportDashboardItems { get; }
    DbSet<ReportDashboardVersion> ReportDashboardVersions { get; }
    DbSet<ReportVersion> ReportVersions { get; }
    DbSet<ReportView> ReportViews { get; }
    DbSet<ReportFavorite> ReportFavorites { get; }
    DbSet<ReportComment> ReportComments { get; }
    DbSet<ReportPermission> ReportPermissions { get; }
    DbSet<ReportExecution> ReportExecutions { get; }
    DbSet<ReportAudit> ReportAudits { get; }
    DbSet<ReportDashboardAudit> ReportDashboardAudits { get; }
    DbSet<ReportDashboardFavorite> ReportDashboardFavorites { get; }
    DbSet<ReportDashboardSchedule> ReportDashboardSchedules { get; }
    DbSet<ReportSubscription> ReportSubscriptions { get; }
    DbSet<ReportDashboardSubscription> ReportDashboardSubscriptions { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
} 