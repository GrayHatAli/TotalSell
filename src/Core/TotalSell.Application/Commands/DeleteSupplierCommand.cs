using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteSupplierCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 