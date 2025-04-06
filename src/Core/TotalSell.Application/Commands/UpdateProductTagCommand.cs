namespace TotalSell.Application.Commands;

public class UpdateProductTagCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public string? Color { get; set; }
    public bool IsActive { get; set; }
} 