using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteCustomerCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 