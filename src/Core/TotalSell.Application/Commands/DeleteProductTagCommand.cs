using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteProductTagCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 