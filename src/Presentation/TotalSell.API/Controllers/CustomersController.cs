using Microsoft.AspNetCore.Mvc;
using TotalSell.Application.Commands;
using TotalSell.Application.Queries;
using TotalSell.Application.DTOs;
using MediatR;

namespace TotalSell.API.Controllers;

public class CustomersController : BaseController
{
    public CustomersController(IMediator mediator) : base(mediator)
    {
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<CustomerDto>>> GetCustomers()
    {
        var query = new SearchCustomersQuery();
        var result = await _mediator.Send(query);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<CustomerDto>> GetCustomer(Guid id)
    {
        var query = new GetCustomerQuery { CustomerId = id };
        var result = await _mediator.Send(query);
        if (result == null)
            return NotFound();
        return Ok(result);
    }

    [HttpPost]
    public async Task<ActionResult<Guid>> CreateCustomer(CreateCustomerCommand command)
    {
        var result = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetCustomer), new { id = result }, result);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult> UpdateCustomer(Guid id, UpdateCustomerCommand command)
    {
        if (id != command.CustomerId)
            return BadRequest();
        
        await _mediator.Send(command);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> DeleteCustomer(Guid id)
    {
        var command = new DeleteCustomerCommand { Id = id };
        await _mediator.Send(command);
        return NoContent();
    }
} 