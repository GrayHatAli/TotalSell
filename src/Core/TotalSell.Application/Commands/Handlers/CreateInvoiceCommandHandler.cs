using MediatR;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;
using AutoMapper;

namespace TotalSell.Application.Commands.Handlers;

public class CreateInvoiceCommandHandler : IRequestHandler<CreateInvoiceCommand, Guid>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public CreateInvoiceCommandHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<Guid> Handle(CreateInvoiceCommand request, CancellationToken cancellationToken)
    {
        var invoice = _mapper.Map<Invoice>(request);

        foreach (var itemDto in request.Items)
        {
            var item = InvoiceItem.Create(
                invoice.Id,
                itemDto.ProductId,
                itemDto.Quantity,
                itemDto.UnitPrice,
                itemDto.DiscountAmount,
                itemDto.TaxAmount);
            invoice.AddItem(item);
        }

        _context.Invoices.Add(invoice);
        await _context.SaveChangesAsync(cancellationToken);
        return invoice.Id;
    }
} 