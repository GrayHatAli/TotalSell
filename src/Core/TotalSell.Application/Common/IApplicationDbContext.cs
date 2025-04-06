using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Common;

public interface IApplicationDbContext
{
    DbSet<Customer> Customers { get; set; }
    DbSet<ReportCategory> ReportCategories { get; set; }
    DbSet<Report> Reports { get; set; }
    DbSet<ReportDashboard> ReportDashboards { get; set; }
    DbSet<ReportDashboardItem> ReportDashboardItems { get; set; }
    DbSet<ReportDashboardVersion> ReportDashboardVersions { get; }
    DbSet<ReportVersion> ReportVersions { get; set; }
    DbSet<ReportView> ReportViews { get; set; }
    DbSet<ReportFavorite> ReportFavorites { get; set; }
    DbSet<ReportComment> ReportComments { get; set; }
    DbSet<ReportPermission> ReportPermissions { get; set; }
    DbSet<ReportExecution> ReportExecutions { get; set; }
    DbSet<ReportAudit> ReportAudits { get; set; }
    DbSet<ReportDashboardAudit> ReportDashboardAudits { get; set; }
    DbSet<ReportDashboardFavorite> ReportDashboardFavorites { get; set; }
    DbSet<ReportDashboardSchedule> ReportDashboardSchedules { get; set; }
    DbSet<ReportSubscription> ReportSubscriptions { get; set; }
    DbSet<ReportDashboardSubscription> ReportDashboardSubscriptions { get; set; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
} 