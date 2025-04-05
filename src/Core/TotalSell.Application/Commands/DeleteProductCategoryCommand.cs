using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteProductCategoryCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 