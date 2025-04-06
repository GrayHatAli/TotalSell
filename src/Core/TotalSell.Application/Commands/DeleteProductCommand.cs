using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteProductCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 