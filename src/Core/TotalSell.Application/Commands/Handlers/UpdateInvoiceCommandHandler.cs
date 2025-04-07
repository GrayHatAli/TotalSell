using MediatR;
using Microsoft.EntityFrameworkCore;
using TotalSell.Application.Common;
using TotalSell.Application.Commands;
using TotalSell.Domain.Entities;
using AutoMapper;

namespace TotalSell.Application.Commands.Handlers;

public class UpdateInvoiceCommandHandler : IRequestHandler<UpdateInvoiceCommand, Unit>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public UpdateInvoiceCommandHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<Unit> Handle(UpdateInvoiceCommand request, CancellationToken cancellationToken)
    {
        var invoice = await _context.Invoices
            .Include(i => i.Items)
            .FirstOrDefaultAsync(i => i.Id == request.Id, cancellationToken);

        if (invoice == null)
            throw new KeyNotFoundException($"Invoice with ID {request.Id} not found.");

        _mapper.Map(request, invoice);

        // Remove items that are no longer in the request
        var itemsToRemove = invoice.Items.Where(item => !request.Items.Any(i => i.ProductId == item.ProductId)).ToList();
        foreach (var item in itemsToRemove)
        {
            invoice.RemoveItem(item);
        }

        // Update or add items
        foreach (var itemDto in request.Items)
        {
            var existingItem = invoice.Items.FirstOrDefault(i => i.ProductId == itemDto.ProductId);
            if (existingItem != null)
            {
                existingItem.Update(
                    itemDto.Quantity,
                    itemDto.UnitPrice,
                    itemDto.DiscountAmount,
                    itemDto.TaxAmount);
            }
            else
            {
                var newItem = InvoiceItem.Create(
                    invoice.Id,
                    itemDto.ProductId,
                    itemDto.Quantity,
                    itemDto.UnitPrice,
                    itemDto.DiscountAmount,
                    itemDto.TaxAmount);
                invoice.AddItem(newItem);
            }
        }

        await _context.SaveChangesAsync(cancellationToken);
        return Unit.Value;
    }
} 