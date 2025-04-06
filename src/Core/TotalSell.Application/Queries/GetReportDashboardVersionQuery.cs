using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class GetReportDashboardVersionQuery : BaseQuery
{
    public Guid VersionId { get; set; }
} 