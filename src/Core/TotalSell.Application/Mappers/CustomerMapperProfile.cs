using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class CustomerMapperProfile : Profile
{
    public CustomerMapperProfile()
    {
        CreateMap<Customer, CustomerDto>()
            .ReverseMap();
    }
} 