using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class SupplierMapperProfile : Profile
{
    public SupplierMapperProfile()
    {
        CreateMap<Supplier, SupplierDto>()
            .ReverseMap();
    }
} 