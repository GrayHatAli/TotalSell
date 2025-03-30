namespace TotalSell.Domain.Entities;

public class Customer : BaseEntity
{
    public string Name { get; private set; }
    public string Code { get; private set; }
    public string NationalCode { get; private set; }
    public string EconomicCode { get; private set; }
    public string PhoneNumber { get; private set; }
    public string MobileNumber { get; private set; }
    public string Email { get; private set; }
    public string Address { get; private set; }
    public string PostalCode { get; private set; }
    public bool IsActive { get; private set; }

    private Customer() { }

    public Customer(
        string name,
        string code,
        string nationalCode,
        string economicCode,
        string phoneNumber,
        string mobileNumber,
        string email,
        string address,
        string postalCode)
    {
        Name = name;
        Code = code;
        NationalCode = nationalCode;
        EconomicCode = economicCode;
        PhoneNumber = phoneNumber;
        MobileNumber = mobileNumber;
        Email = email;
        Address = address;
        PostalCode = postalCode;
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string nationalCode,
        string economicCode,
        string phoneNumber,
        string mobileNumber,
        string email,
        string address,
        string postalCode)
    {
        Name = name;
        Code = code;
        NationalCode = nationalCode;
        EconomicCode = economicCode;
        PhoneNumber = phoneNumber;
        MobileNumber = mobileNumber;
        Email = email;
        Address = address;
        PostalCode = postalCode;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 