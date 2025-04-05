using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteProductBrandCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 