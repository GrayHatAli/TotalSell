using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Common.Persistence;

public interface IApplicationDbContext
{
    DbSet<Invoice> Invoices { get; set; }
    DbSet<InvoiceItem> InvoiceItems { get; set; }
    DbSet<Customer> Customers { get; set; }
    DbSet<Product> Products { get; set; }
    DbSet<ReportCategory> ReportCategories { get; set; }
    DbSet<Report> Reports { get; set; }
    DbSet<ReportDashboard> ReportDashboards { get; set; }
    DbSet<ReportDashboardItem> ReportDashboardItems { get; set; }
    DbSet<ReportDashboardVersion> ReportDashboardVersions { get; set; }
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
} 