namespace TotalSell.Application.Commands;

public class CreateProductBrandCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public string? Website { get; set; }
    public string? Logo { get; set; }
} 