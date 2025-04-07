using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteInvoiceCommand : BaseCommand, IRequest<Unit>
{
    public new required Guid Id { get; set; }
} 