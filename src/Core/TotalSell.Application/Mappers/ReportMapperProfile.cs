using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class ReportMapperProfile : Profile
{
    public ReportMapperProfile()
    {
        CreateMap<Report, ReportDto>()
            .ForMember(dest => dest.CreatedByName, opt => opt.MapFrom(src => src.CreatedBy))
            .ForMember(dest => dest.ApprovedByName, opt => opt.MapFrom(src => src.ApprovedBy))
            .ForMember(dest => dest.Parameters, opt => opt.MapFrom(src => src.Parameters))
            .ForMember(dest => dest.Filters, opt => opt.MapFrom(src => src.Filters))
            .ReverseMap();
    }
} 