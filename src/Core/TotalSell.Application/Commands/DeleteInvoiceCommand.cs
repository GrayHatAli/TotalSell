using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteInvoiceCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 