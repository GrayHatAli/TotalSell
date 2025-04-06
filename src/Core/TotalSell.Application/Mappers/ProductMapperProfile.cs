using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;
namespace TotalSell.Application.Mappers;

public class ProductMapperProfile : Profile
{
    public ProductMapperProfile()
    {
        CreateMap<Product, ProductDto>()
            .ForMember(dest => dest.CategoryName, opt => opt.MapFrom(src => src.Category != null ? src.Category.Name : null))
            .ForMember(dest => dest.BrandName, opt => opt.MapFrom(src => src.Brand != null ? src.Brand.Name : null))
            .ForMember(dest => dest.Tags, opt => opt.MapFrom(src => src.ProductTags != null ? src.ProductTags.Select(pt => pt.Tag != null ? pt.Tag.Name : null).Where(name => name != null) : null))
            .ReverseMap();
    }
} 