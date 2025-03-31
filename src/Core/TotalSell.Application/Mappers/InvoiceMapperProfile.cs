using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class InvoiceMapperProfile : Profile
{
    public InvoiceMapperProfile()
    {
        CreateMap<Invoice, InvoiceDto>()
            .ForMember(dest => dest.CustomerName, opt => opt.MapFrom(src => src.Customer.Name))
            .ForMember(dest => dest.Items, opt => opt.MapFrom(src => src.Items.Select(item => new InvoiceItemDto
            {
                ProductId = item.ProductId,
                ProductName = item.Product.Name,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice,
                DiscountAmount = item.DiscountAmount,
                TaxAmount = item.TaxAmount,
                TotalAmount = item.TotalAmount
            })))
            .ReverseMap();
    }
} 