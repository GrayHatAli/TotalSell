using Microsoft.EntityFrameworkCore;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<ReportDashboardVersion> ReportDashboardVersions { get; }
    
    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
} 