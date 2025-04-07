using AutoMapper;
using TotalSell.Application.Commands;
using TotalSell.Application.DTOs;
using TotalSell.Domain.Entities;
using TotalSell.Domain.Enums;

namespace TotalSell.Application.Mappers;

public class InvoiceMapperProfile : Profile
{
    public InvoiceMapperProfile()
    {
        CreateMap<CreateInvoiceCommand, SalesInvoice>()
            .ConstructUsing((src, ctx) => SalesInvoice.Create(
                src.Number,
                src.Date,
                src.CustomerId,
                src.Description,
                src.PaymentTerms,
                src.DueDate));

        CreateMap<UpdateInvoiceCommand, Invoice>()
            .ConstructUsing((src, ctx) => SalesInvoice.Create(
                src.Number,
                src.Date,
                src.CustomerId,
                src.Description,
                src.PaymentTerms,
                src.DueDate));

        CreateMap<Invoice, InvoiceDto>();
        CreateMap<InvoiceItem, InvoiceItemDto>();
    }
} 