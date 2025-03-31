using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateSupplierCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? NationalCode { get; set; }
    public string? EconomicCode { get; set; }
    public string? Email { get; set; }
    public string? PhoneNumber { get; set; }
    public string? MobileNumber { get; set; }
    public string? Address { get; set; }
    public string? PostalCode { get; set; }
    public string? Description { get; set; }
} 