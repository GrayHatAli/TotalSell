using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class GetReportDashboardItemQuery : BaseQuery
{
    public Guid ItemId { get; set; }
} 