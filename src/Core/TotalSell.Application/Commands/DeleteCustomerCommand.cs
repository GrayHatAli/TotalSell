using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteCustomerCommand : BaseCommand
{
    public Guid Id { get; set; }
} 