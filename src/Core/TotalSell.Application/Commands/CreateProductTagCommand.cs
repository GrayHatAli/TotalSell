using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateProductTagCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public string? Color { get; set; }
} 