using AutoMapper;
using TotalSell.Application.Commands;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;
namespace TotalSell.Application.Mappers;

public class ProductMapperProfile : Profile
{
    public ProductMapperProfile()
    {
        CreateMap<CreateProductCommand, Product>()
            .ConstructUsing((src, ctx) => Product.Create(
                src.Name,
                src.Code,
                src.Description,
                src.Price,
                src.DiscountedPrice,
                src.Barcode,
                src.SKU,
                src.Brand,
                src.Category,
                src.Unit,
                src.StockQuantity,
                src.MinimumStockQuantity,
                src.IsActive,
                src.Tags));

        CreateMap<UpdateProductCommand, Product>()
            .ConstructUsing((src, ctx) => Product.Create(
                src.Name,
                src.Code,
                src.Description,
                src.Price,
                src.DiscountedPrice,
                src.Barcode,
                src.SKU,
                src.Brand,
                src.Category,
                src.Unit,
                src.StockQuantity,
                src.MinimumStockQuantity,
                src.IsActive,
                src.Tags));

        CreateMap<Product, ProductDto>();
    }
} 