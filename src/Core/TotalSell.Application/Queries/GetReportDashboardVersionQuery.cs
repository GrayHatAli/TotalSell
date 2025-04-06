using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.DTOs;

namespace TotalSell.Application.Queries;

public class GetReportDashboardVersionQuery : BaseQuery, IRequest<ReportDashboardVersionDto>
{
    public Guid VersionId { get; set; }
} 