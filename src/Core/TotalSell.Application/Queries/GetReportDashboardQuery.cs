using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class GetReportDashboardQuery : BaseQuery
{
    public Guid DashboardId { get; set; }
} 