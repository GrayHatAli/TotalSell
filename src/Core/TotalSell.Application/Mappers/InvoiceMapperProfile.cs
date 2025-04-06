using AutoMapper;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;

namespace TotalSell.Application.Mappers;

public class InvoiceMapperProfile : Profile
{
    public InvoiceMapperProfile()
    {
        CreateMap<SalesInvoice, InvoiceDto>()
            .ForMember(dest => dest.CustomerName, opt => opt.MapFrom(src => src.Customer != null ? src.Customer.Name : string.Empty))
            .ForMember(dest => dest.Items, opt => opt.MapFrom(src => src.Items.Select(item => new InvoiceItemDto
            {
                ProductId = item.ProductId,
                ProductName = item.Product != null ? item.Product.Name : string.Empty,
                Quantity = item.Quantity,
                UnitPrice = item.UnitPrice,
                DiscountAmount = item.DiscountAmount,
                TaxAmount = item.TaxAmount,
                TotalAmount = item.TotalAmount
            })))
            .ReverseMap();
    }
} 