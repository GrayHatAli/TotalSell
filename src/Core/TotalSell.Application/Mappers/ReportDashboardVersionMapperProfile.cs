using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class ReportDashboardVersionMapperProfile : Profile
{
    public ReportDashboardVersionMapperProfile()
    {
        CreateMap<ReportDashboardVersion, ReportDashboardVersionDto>();
        CreateMap<ReportDashboardVersion, ReportDashboardVersionSummaryDto>();
    }
} 