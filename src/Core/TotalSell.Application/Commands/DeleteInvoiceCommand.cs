using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteInvoiceCommand : BaseCommand, IRequest<bool>
{
    public new required Guid Id { get; set; }
} 